# Copyright (c) 2020-2021, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import requests
import sys
import getopt
import time
import os
import subprocess
from clusterutils import ClusterUtils
import params


def main():

  master_addr = ClusterUtils.cluster_get_master_addr(params.workspace, params.clusterid, params.token)
  if master_addr is None:
      print("Error, didn't get master address")
      sys.exit(1)
  print("Master node address is: %s" % master_addr)

  print("Copying script")
  rsync_command = "rsync -I -Pave \"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2200 -i %s\" %s ubuntu@%s:%s" % (params.private_key_file, params.local_script, master_addr, params.script_dest)
  print("rsync command: %s" % rsync_command)
  subprocess.check_call(rsync_command, shell = True)

  ssh_command = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ubuntu@%s -p 2200 -i %s 'LOCAL_JAR_PATH=%s SPARK_CONF=%s BASE_SPARK_VER=%s bash %s 2>&1 | tee testout; if [ ${PIPESTATUS[0]} -ne 0 ]; then false; else true; fi'" % (master_addr, params.private_key_file, params.jar_path, params.spark_conf, params.base_spark_pom_version, params.script_dest)
  print("ssh command: %s" % ssh_command)
  subprocess.check_call(ssh_command, shell = True)

if __name__ == '__main__':
  main()
