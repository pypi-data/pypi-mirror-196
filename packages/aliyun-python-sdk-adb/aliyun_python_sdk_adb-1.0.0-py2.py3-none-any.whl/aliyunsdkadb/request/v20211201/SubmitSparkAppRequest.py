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

class SubmitSparkAppRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'adb', '2021-12-01', 'SubmitSparkApp','ads')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ResourceGroupName(self): # String
		return self.get_body_params().get('ResourceGroupName')

	def set_ResourceGroupName(self, ResourceGroupName):  # String
		self.add_body_params('ResourceGroupName', ResourceGroupName)
	def get_AgentVersion(self): # String
		return self.get_body_params().get('AgentVersion')

	def set_AgentVersion(self, AgentVersion):  # String
		self.add_body_params('AgentVersion', AgentVersion)
	def get_Data(self): # String
		return self.get_body_params().get('Data')

	def set_Data(self, Data):  # String
		self.add_body_params('Data', Data)
	def get_AppName(self): # String
		return self.get_body_params().get('AppName')

	def set_AppName(self, AppName):  # String
		self.add_body_params('AppName', AppName)
	def get_TemplateFileId(self): # Long
		return self.get_body_params().get('TemplateFileId')

	def set_TemplateFileId(self, TemplateFileId):  # Long
		self.add_body_params('TemplateFileId', TemplateFileId)
	def get_DBClusterId(self): # String
		return self.get_body_params().get('DBClusterId')

	def set_DBClusterId(self, DBClusterId):  # String
		self.add_body_params('DBClusterId', DBClusterId)
	def get_AppType(self): # String
		return self.get_body_params().get('AppType')

	def set_AppType(self, AppType):  # String
		self.add_body_params('AppType', AppType)
	def get_AgentSource(self): # String
		return self.get_body_params().get('AgentSource')

	def set_AgentSource(self, AgentSource):  # String
		self.add_body_params('AgentSource', AgentSource)
