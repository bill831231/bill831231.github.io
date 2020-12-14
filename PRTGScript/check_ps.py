import json
import sys
import logging
from panos.firewall import Firewall
from prtg.sensor.result import CustomSensorResult
from prtg.sensor.units import ValueUnit
import lxml.etree as ET
logging.basicConfig(filename="Power_supply_sensor_debug.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y:%M:%D:%H:%M:%S',
                            level=logging.INFO)
if __name__ == "__main__":
    try:
        data = json.loads(sys.argv[1])
        username = data['linuxloginusername']
        passwd = data['linuxloginpassword']
        host = data['host']
        fw = Firewall(host, api_username=username, api_password=passwd)
        env_info = fw.op("show system environmentals",xml=True)
        env_decode = env_info.decode("utf-8")
        tree = ET.fromstring(str(env_decode))
        ps_items = tree.xpath(".//power-supply/Slot1/entry/description")
        ps_status_list = []
        for ps_item in ps_items:
            ps_status = []
            ps_des = ''.join(ps_item.itertext())
            ps_status.append(ps_des)
            for sb_item in ps_item.itersiblings(preceding=True):
                ps_status.append(sb_item.text)
            ps_status_list.append(ps_status)
        num_ps_found = len(ps_status_list)

        csr = CustomSensorResult(text="This sensor runs on {}".format(data["host"]))
        csr.add_primary_channel(name="Node need {} Power supplies".format(num_ps_found),
                                value=num_ps_found,
                                unit=ValueUnit.CUSTOM,
                                is_limit_mode=True,
                                limit_min_error=num_ps_found,
                                show_table=False,
                                limit_error_msg="power module is missing")
        
        for channel in range(num_ps_found):
            power_supply_item = ps_status_list.pop()
            p_name = power_supply_item[0]
            if power_supply_item[1] == "True":
                insert_status = 1
            else:
                insert_status = 0
            if power_supply_item[2] == "True":
                alarm_status = 1
            else:
                alarm_status = 0
            csr.add_channel(name="{} insert status".format(p_name),
                        value=insert_status,
                        unit=ValueUnit.CUSTOM,
                        is_float=False,
                        is_limit_mode=True,
                        limit_min_error=1,
                        limit_error_msg="power module {} is not in place".format(p_name))
            csr.add_channel(name="{} alarm status".format(p_name),
                        value=alarm_status,
                        unit=ValueUnit.CUSTOM,
                        is_float=False,
                        is_limit_mode=True,
                        limit_max_error=0,
                        limit_error_msg="alarm on module {}".format(p_name))

        logging.debug(csr.json_result)
    except Exception as e:
        csr = CustomSensorResult(text="Python Script execution error")
        csr.error = "Python Script execution error: %s" % str(e)
        logging.debug(csr.json_result)
