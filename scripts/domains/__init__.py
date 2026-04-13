'''
Windchill PLM Domain-Specific Clients

This package contains domain-specific clients for Windchill PLM:
- ProdMgmt: Product Management (Parts, BOM)
- DocMgmt: Document Management
- CADDocumentMgmt: CAD Document Management
- ChangeMgmt: Change Management
- SupplierMgmt: Supplier Management
- MfgProcMgmt: Manufacturing Process Management
- CEM: Customer Experience Management
- BACMgmt: Baseline and Configuration Management
- Workflow: Workflow and Lifecycle
- Audit: Audit Management
- DataAdmin: Data Administration
- ServiceInfoMgmt: Service Information Management
- UDI: Unique Device Identification
- RegMstr: Regulatory Master
- QMS: Quality Management System
- PrincipalMgmt: Principal Management (Users, Groups, Roles)
- PTC: Common PTC namespace (shared entities, content management, base types)
'''
# Copyright 2025 Windchill PLM Client Contributors
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

from .ProdMgmt import ProdMgmtClient, create_prodmgmt_client
from .DocMgmt import DocMgmtClient, create_docmgmt_client
from .CADDocumentMgmt import CADDocumentMgmtClient, create_cad_documentmgmt_client
from .ChangeMgmt import ChangeMgmtClient, create_changemgmt_client
from .SupplierMgmt import SupplierMgmtClient, create_suppliermgmt_client
from .MfgProcMgmt import MfgProcMgmtClient, create_mfgprocmgmt_client
from .CEM import CEMClient, create_cem_client
from .BACMgmt import BACMgmtClient, create_bacmgmt_client
from .Workflow import WorkflowClient, create_workflow_client
from .Audit import AuditClient, create_audit_client
from .DataAdmin import DataAdminClient, create_dataadmin_client
from .ServiceInfoMgmt import ServiceInfoMgmtClient, create_serviceinfomgmt_client
from .UDI import UDIClient, create_udi_client
from .RegMstr import RegMstrClient, create_regmstr_client
from .QMS import QMSClient, create_qms_client
from .PrincipalMgmt import PrincipalMgmtClient, create_principalmgmt_client
from .PTC import PTCClient, create_ptc_client

__all__ = [
 'ProdMgmtClient', 'create_prodmgmt_client',
 'DocMgmtClient', 'create_docmgmt_client',
 'CADDocumentMgmtClient', 'create_cad_documentmgmt_client',
 'ChangeMgmtClient', 'create_changemgmt_client',
 'SupplierMgmtClient', 'create_suppliermgmt_client',
 'MfgProcMgmtClient', 'create_mfgprocmgmt_client',
 'CEMClient', 'create_cem_client',
 'BACMgmtClient', 'create_bacmgmt_client',
 'WorkflowClient', 'create_workflow_client',
 'AuditClient', 'create_audit_client',
 'DataAdminClient', 'create_dataadmin_client',
 'ServiceInfoMgmtClient', 'create_serviceinfomgmt_client',
 'UDIClient', 'create_udi_client',
 'RegMstrClient', 'create_regmstr_client',
 'QMSClient', 'create_qms_client',
 'PrincipalMgmtClient', 'create_principalmgmt_client',
 'PTCClient', 'create_ptc_client',
]
