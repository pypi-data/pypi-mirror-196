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

class GetTableObjectsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'adb', '2021-12-01', 'GetTableObjects','ads')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_PageNumber(self): # Long
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self, PageNumber):  # Long
		self.add_query_param('PageNumber', PageNumber)
	def get_FilterTblType(self): # String
		return self.get_query_params().get('FilterTblType')

	def set_FilterTblType(self, FilterTblType):  # String
		self.add_query_param('FilterTblType', FilterTblType)
	def get_FilterDescription(self): # String
		return self.get_query_params().get('FilterDescription')

	def set_FilterDescription(self, FilterDescription):  # String
		self.add_query_param('FilterDescription', FilterDescription)
	def get_PageSize(self): # Long
		return self.get_query_params().get('PageSize')

	def set_PageSize(self, PageSize):  # Long
		self.add_query_param('PageSize', PageSize)
	def get_FilterTblName(self): # String
		return self.get_query_params().get('FilterTblName')

	def set_FilterTblName(self, FilterTblName):  # String
		self.add_query_param('FilterTblName', FilterTblName)
	def get_SchemaName(self): # String
		return self.get_query_params().get('SchemaName')

	def set_SchemaName(self, SchemaName):  # String
		self.add_query_param('SchemaName', SchemaName)
	def get_DBClusterId(self): # String
		return self.get_query_params().get('DBClusterId')

	def set_DBClusterId(self, DBClusterId):  # String
		self.add_query_param('DBClusterId', DBClusterId)
	def get_OrderBy(self): # String
		return self.get_query_params().get('OrderBy')

	def set_OrderBy(self, OrderBy):  # String
		self.add_query_param('OrderBy', OrderBy)
	def get_FilterOwner(self): # String
		return self.get_query_params().get('FilterOwner')

	def set_FilterOwner(self, FilterOwner):  # String
		self.add_query_param('FilterOwner', FilterOwner)
