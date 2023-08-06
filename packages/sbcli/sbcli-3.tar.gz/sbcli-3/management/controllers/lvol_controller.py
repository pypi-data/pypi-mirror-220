# coding=utf-8
import datetime
import logging as lg
import json
import string
import random
import sys
import time

from management import utils, constants
from management.kv_store import DBController
from management.models.pool import Pool
from management.models.storage_node import LVol
from management.rpc_client import RPCClient

logger = lg.getLogger()

db_controller = DBController()


def _generate_hex_string(length):
    def _generate_string(length):
        return ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(length))

    return _generate_string(length).encode('utf-8').hex()


def _create_crypto_lvol(rpc_client, name, base_name):
    key_name = f'key_{name}'
    key1 = _generate_hex_string(32)
    key2 = _generate_hex_string(32)
    ret = rpc_client.lvol_crypto_key_create(key_name, key1, key2)
    if not ret:
        logger.warning("failed to create crypto key")
    ret = rpc_client.lvol_crypto_create(name, base_name, key_name)
    if not ret:
        logger.error(f"failed to create crypto LVol {name}")
        return False
    return ret


def _create_compress_lvol(rpc_client, base_bdev_name):
    pm_path = constants.PMEM_DIR
    ret = rpc_client.lvol_compress_create(base_bdev_name, pm_path)
    if not ret:
        logger.error("failed to create compress LVol on the storage node")
        return False
    return ret


def ask_for_device_number(devices_list):
    question = f"Enter the device number [1-{len(devices_list)}]: "
    while True:
        sys.stdout.write(question)
        choice = str(input())
        try:
            ch = int(choice.strip())
            ch -= 1
            return devices_list[ch]
        except Exception as e:
            logger.debug(e)
            sys.stdout.write(f"Please respond with numbers 1 - {len(devices_list)}\n")


def ask_for_lvol_vuid():
    question = f"Enter VUID number: "
    while True:
        sys.stdout.write(question)
        choice = str(input())
        try:
            ch = int(choice.strip())
            return ch
        except Exception as e:
            logger.debug(e)
            sys.stdout.write(f"Please respond with numbers")


def add_lvol(name, size, hostname, pool_id_or_name, use_comp, use_crypto,
             distr, distr_vuid, distr_ndcs, distr_npcs, distr_alcemel_count,
             max_w_iops, max_r_iops, max_r_mbytes, max_w_mbytes):
    # TODO: implement qos params
    logger.info("adding LVol")
    snode = db_controller.get_storage_node_by_hostname(hostname)
    if not snode:
        logger.error("can not find storage node")
        return False

    pool = None
    if pool_id_or_name:
        for p in db_controller.get_pools():
            if pool_id_or_name == p.id or pool_id_or_name == p.pool_name:
                pool = p
                break
        if not pool:
            logger.error(f"Pool not found: {pool_id_or_name}")
            return False

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    if not snode.nvme_devices:
        logger.error("Storage node has no nvme devices")
        return False

    lvol = LVol()
    lvol.lvol_name = name
    lvol.size = size

    bdev_stack = []
    if distr is True:
        vuid = 100
        if distr_vuid:
            vuid = distr_vuid

        num_blocks = int(size / 512)
        alloc_names = []
        for i in range(distr_alcemel_count):
            nm = f"alceml_{name}_{(i + 1)}"
            ret = rpc_client.bdev_alceml_create(nm, vuid + (i + 1), num_blocks)
            if not ret:
                logger.error("failed to create Alceml bdev")
                return False
            alloc_names.append(nm)
            bdev_stack.append({"type": "alceml", "name": nm})
            time.sleep(3)

        names = ",".join(alloc_names)
        ret = rpc_client.bdev_distrib_create(f"distr_{name}", vuid, distr_ndcs, distr_npcs, num_blocks, names)
        bdev_stack.append({"type": "distr", "name": f"distr_{name}"})
        if not ret:
            logger.error("failed to create Distr bdev")
            return False

        time.sleep(5)
        ret = rpc_client.create_lvstore(f"LVS_{vuid}", f"distr_{name}")
        bdev_stack.append({"type": "lvs", "name": f"LVS_{vuid}"})
        if not ret:
            logger.error("failed to create lvs")
            # return False
        lvol.base_bdev = f"distr_{name}"

    else:
        nvme_dev = None
        if len(snode.nvme_devices) == 1:
            nvme_dev = snode.nvme_devices[0]
        else:
            nvme_dev = ask_for_device_number(snode.nvme_devices)

        vuid = ask_for_lvol_vuid()

        ret = rpc_client.ultra21_bdev_pass_create(nvme_dev.alloc_bdev, vuid, f"ultra_pt_{vuid}")
        bdev_stack.append({"type": "ultra_pt", "name": f"ultra_pt_{vuid}"})
        if not ret:
            logger.error("failed to create PT on the storage node")
            return False

        ret = rpc_client.create_lvstore(f"LVS_{vuid}", f"ultra_pt_{vuid}")
        bdev_stack.append({"type": "lvs", "name": f"LVS_{vuid}"})
        if not ret:
            logger.error("failed to create lvs on the storage node")
            return False
        lvol.base_bdev = nvme_dev.alloc_bdev
        lvol.nvme_dev = nvme_dev

    ret = rpc_client.create_lvol(name, size, f"LVS_{vuid}")
    bdev_stack.append({"type": "lvol", "name": f"LVS_{vuid}/{name}"})

    if not ret:
        logger.error("failed to create LVol on the storage node")
        return False
    lvol_id = ret

    lvol_type = 'lvol'
    lvol_bdev = f"LVS_{vuid}/{name}"
    crypto_bdev = ''
    comp_bdev = ''
    top_bdev = lvol_bdev
    if use_crypto is True:
        crypto_bdev = _create_crypto_lvol(rpc_client, name, lvol_bdev)
        bdev_stack.append({"type": "crypto", "name": crypto_bdev})
        if not crypto_bdev:
            return False
        lvol_type += ',crypto'
        top_bdev = crypto_bdev

    if use_comp is True:
        n = crypto_bdev if crypto_bdev else lvol_bdev
        comp_bdev = _create_compress_lvol(rpc_client, n)
        bdev_stack.append({"type": "comp", "name": comp_bdev})
        if not comp_bdev:
            return False
        lvol_type += ',compress'
        top_bdev = comp_bdev

    # add lvol to subsystem
    logger.info(f"add lvol {name} to subsystem")
    ret = rpc_client.nvmf_subsystem_add_ns(snode.subsystem, top_bdev)

    lvol.bdev_stack = bdev_stack
    lvol.uuid = lvol_id
    lvol.lvol_bdev = lvol_bdev
    lvol.crypto_bdev = crypto_bdev
    lvol.comp_bdev = comp_bdev
    lvol.hostname = snode.hostname
    lvol.node_id = snode.get_id()
    lvol.mode = 'read-write'
    lvol.lvol_type = lvol_type
    if pool:
        lvol.pool_uuid = pool.id
        pool.lvols.append(lvol_id)
        pool.write_to_db(db_controller.kv_store)

    lvol.write_to_db(db_controller.kv_store)

    snode.lvols.append(lvol_id)
    snode.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return lvol_id


def delete_lvol(uuid, force_delete=False):
    lvol = db_controller.get_lvol_by_id(uuid)
    if not lvol:
        logger.error(f"lvol not found: {uuid}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False


    logger.debug(lvol)
    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    for bdev in lvol.bdev_stack[::-1]:
        type = bdev['type']
        name = bdev['name']
        if type == "alceml":
            ret = rpc_client.bdev_alceml_delete(name)
            if not ret:
                logger.error(f"failed to delete alceml: {name}")
            continue
        if type == "distr":
            ret = rpc_client.bdev_distrib_delete(name)
            if not ret:
                logger.error(f"failed to delete distr: {name}")
            continue
        if type == "lvs":
            ret = rpc_client.bdev_lvol_delete_lvstore(name)
            if not ret:
                logger.error(f"failed to delete lvs: {name}")
            continue
        if type == "lvol":
            ret = rpc_client.delete_lvol(name)
            if not ret:
                logger.error(f"failed to delete lvol bdev {name}")
            continue
        if type == "ultra_pt":
            ret = rpc_client.ultra21_bdev_pass_delete(name)
            if not ret:
                logger.error(f"failed to delete ultra pt {name}")
            continue
        if type == "comp":
            ret = rpc_client.lvol_compress_delete(name)
            if not ret:
                logger.error(f"failed to delete comp bdev {name}")
            continue
        if type == "crypto":
            ret = rpc_client.lvol_crypto_delete(name)
            if not ret:
                logger.error(f"failed to delete crypto bdev {name}")
            continue

    # remove from storage node
    snode.lvols.remove(uuid)
    snode.write_to_db(db_controller.kv_store)

    # remove from pool
    pool.lvols.remove(uuid)
    pool.write_to_db(db_controller.kv_store)

    lvol.remove(db_controller.kv_store)
    logger.info("Done")
    return True


def set_lvol(uuid, max_rw_iops, max_rw_mbytes, max_r_mbytes, max_w_mbytes):
    # TODO: implement
    pass


def list_lvols(is_json):
    lvols = db_controller.get_lvols()
    data = []
    for lvol in lvols:
        logger.debug(lvol)
        data.append({
            "id": lvol.uuid,
            "name": lvol.lvol_name,
            "size": utils.humanbytes(lvol.size),
            "pool": lvol.pool_uuid,
            "hostname": lvol.hostname,
            "types": lvol.lvol_type,
            "status": "on",
        })

    if is_json:
        return json.dumps(data, indent=2)
    else:
        return utils.print_table(data)


def get_lvol(lvol_id, is_json):
    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error(f"lvol not found: {lvol_id}")
        return False

    data = lvol.get_clean_dict()

    del data['nvme_dev']

    if is_json:
        return json.dumps(data, indent=2)
    else:
        data2 = [{"key": key, "value": data[key]} for key in data]
        return utils.print_table(data2)


def connect_lvol(uuid):
    lvol = db_controller.get_lvol_by_id(uuid)
    if not lvol:
        logger.error(f"lvol not found: {uuid}")
        return False

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)
    out = ""
    for nic in snode.data_nics:
        ip = nic.ip4_address
        out += f"sudo nvme connect --transport=tcp --traddr={ip} --trsvcid=4420 --nqn={snode.subsystem}\n"
    return out


def resize_lvol(id, new_size):
    lvol = db_controller.get_lvol_by_id(id)
    if not lvol:
        logger.error(f"LVol not found: {id}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    if lvol.size <= new_size:
        logger.error(f"New size {new_size} must be higher than the original size {lvol.size}")
        return False

    logger.info(f"Resizing LVol: {lvol.id}, new size: {lvol.size}")

    # if lvol.pool_uuid:
    #     pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    #     if pool:
    #         print(pool)

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    # ret = rpc_client.get_bdevs(lvol.lvol_name)
    # bdev_data = ret[0]
    # logger.debug(json.dumps(ret, indent=2))
    # print("is claimed:", bdev_data['claimed'])
    ret = rpc_client.resize_lvol(lvol.lvol_name, new_size / (1024 * 1024))
    if not ret:
        return "Error"

    lvol.size = new_size
    lvol.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return ret


def set_read_only(id):
    lvol = db_controller.get_lvol_by_id(id)
    if not lvol:
        logger.error(f"LVol not found: {id}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    logger.info(f"Setting LVol: {lvol.id} read only")

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    ret = rpc_client.lvol_read_only(lvol.lvol_name)
    if not ret:
        return "Error"

    lvol.mode = 'read-only'
    lvol.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def create_snapshot(lvol_id, snapshot_name):
    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error(f"LVol not found: {lvol_id}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    logger.info(f"Creating snapshot: {snapshot_name} from LVol: {lvol.id}")

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    ret = rpc_client.lvol_create_snapshot(lvol_id, snapshot_name)
    if not ret:
        return "Error"

    logger.info("Done")
    return ret


def clone(snapshot_name, clone_name):
    lvol = db_controller.get_lvol_by_id(snapshot_name)
    if not lvol:
        logger.error(f"LVol not found: {snapshot_name}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    logger.info(f"Creating LVol {clone_name} from snapshot {snapshot_name}")

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    ret = rpc_client.lvol_clone(snapshot_name, clone_name)
    if not ret:
        return "Error"

    logger.info("Done")
    return ret


def get_capacity(id, history):
    lvol = db_controller.get_lvol_by_id(id)
    if not lvol:
        logger.error(f"lvol not found: {id}")
        return False

    out = [{
        "provisioned": lvol.size,
        "util_percent": 0,
        "util": 0,
    }]

    return utils.print_table(out)


def get_io_stats(lvol_uuid, history):
    lvol = db_controller.get_lvol_by_id(lvol_uuid)
    if not lvol:
        logger.error(f"lvol not found: {lvol_uuid}")
        return False

    data = db_controller.get_lvol_stats(lvol)
    out = []
    if not history:
        data = data[:1]

    for record in data:
        out.append({
            "Date": time.strftime("%H:%M:%S, %d/%m/%Y", time.gmtime(record.date)),
            "bytes_read": record.stats["bytes_read"],
            "read_ops": record.stats["num_read_ops"],
            "read speed /s": utils.humanbytes(record.read_bytes_per_sec),
            "read_ops /s": record.read_iops,
            "bytes_write": record.stats["bytes_written"],
            "write_ops": record.stats["num_write_ops"],
            "write speed /s": utils.humanbytes(record.write_bytes_per_sec),
            "write_ops /s": record.write_iops,
            "read_lat_ticks": record.read_latency_ticks,
            "write_lat_ticks": record.write_latency_ticks,
            "IO Error": record.stats["io_error"],
        })
    return utils.print_table(out)
