# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkadb.endpoint import endpoint_data

class StartSparkSQLEngineRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'adb', '2021-12-01', 'StartSparkSQLEngine','ads')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ResourceGroupName(self): # String
		return self.get_body_params().get('ResourceGroupName')

	def set_ResourceGroupName(self, ResourceGroupName):  # String
		self.add_body_params('ResourceGroupName', ResourceGroupName)
	def get_SlotNum(self): # Long
		return self.get_body_params().get('SlotNum')

	def set_SlotNum(self, SlotNum):  # Long
		self.add_body_params('SlotNum', SlotNum)
	def get_DBClusterId(self): # String
		return self.get_body_params().get('DBClusterId')

	def set_DBClusterId(self, DBClusterId):  # String
		self.add_body_params('DBClusterId', DBClusterId)
	def get_MinExecutor(self): # Long
		return self.get_body_params().get('MinExecutor')

	def set_MinExecutor(self, MinExecutor):  # Long
		self.add_body_params('MinExecutor', MinExecutor)
	def get_Jars(self): # String
		return self.get_body_params().get('Jars')

	def set_Jars(self, Jars):  # String
		self.add_body_params('Jars', Jars)
	def get_MaxExecutor(self): # Long
		return self.get_body_params().get('MaxExecutor')

	def set_MaxExecutor(self, MaxExecutor):  # Long
		self.add_body_params('MaxExecutor', MaxExecutor)
	def get_Config(self): # String
		return self.get_body_params().get('Config')

	def set_Config(self, Config):  # String
		self.add_body_params('Config', Config)
