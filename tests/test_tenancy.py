import pytest
from app.core.tenancy import MunicipalTenancyManager

def test_tenancy_gcc_default():
    tenant = MunicipalTenancyManager.get_tenant("GCC")
    assert tenant["tenant_code"] == "GCC"
    assert "Chennai" in tenant["name_en"]
    assert tenant["helpline"] == "1913"
    assert tenant["total_wards"] == 200

def test_tenancy_coimbatore():
    tenant = MunicipalTenancyManager.get_tenant("CCMC")
    assert tenant["tenant_code"] == "CCMC"
    assert "Coimbatore" in tenant["name_en"]
    assert tenant["total_wards"] == 100

def test_tenancy_fallback():
    tenant = MunicipalTenancyManager.get_tenant("UNKNOWN_CODE")
    assert tenant["tenant_code"] == "GCC"
