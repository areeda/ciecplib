%define name ciecplib
%define version 0.1.0
%define release 1
%define author Duncan Macleod
%define email duncan.macleod@ligo.org

# -- metadata ---------------

BuildArch: noarch
Group:     Development/Libraries
License:   GPL-3.0-or-later
Name:      %{name}
Packager:  %{author} <%{email}>
Prefix:    %{_prefix}
Release:   %{release}%{?dist}
Source0:   https://pypi.io/packages/source/l/%{name}/%{name}-%{version}.tar.gz
Summary:   A python client for SAML ECP authentication
Url:       https://github.com/duncanmmacleod/ciecplib
Vendor:    Duncan Macleod <duncan.macleod@ligo.org>
Version:   %{version}

# -- build requirements -----

BuildRequires: python-srpm-macros
BuildRequires: argparse-manpage

# python2 build
BuildRequires: /usr/bin/python2
BuildRequires: python2-rpm-macros
BuildRequires: python2-setuptools

# python3 build
%if 0%{?rhel} && 0%{?rhel} >= 8
BuildRequires: /usr/bin/python3
BuildRequires: python3-rpm-macros
BuildRequires: python%{python3_pkgversion}-setuptools
%endif

# build requires all runtime dependencies for argparse-manpage
%if 0%{?rhel} && 0%{?rhel} >= 8
BuildRequires: python%{python3_pkgversion}-kerberos
BuildRequires: python%{python3_pkgversion}-lxml
BuildRequires: python%{python3_pkgversion}-m2crypto
BuildRequires: python%{python3_pkgversion}-pyOpenSSL
%else
BuildRequires: m2crypto
BuildRequires: pyOpenSSL
BuildRequires: python-kerberos
BuildRequires: python-lxml
%endif

# -- packages ---------------

# src.rpm
%description
The Python client for SAML ECP authentication.

%package -n python2-%{name}
Summary: %{summary}
Requires: m2crypto
Requires: pyOpenSSL
Requires: python
Requires: python-kerberos
Requires: python-lxml
%{?python_provide:%python_provide python2-%{name}}
%description -n python2-%{name}
The Python %{python2_version} client for SAML ECP authentication.

%if 0%{?rhel} && 0%{?rhel} >= 8
%package -n python%{python3_pkgversion}-%{name}
Summary: %{summary}
Requires: python%{python3_pkgversion}-kerberos
Requires: python%{python3_pkgversion}-lxml
Requires: python%{python3_pkgversion}-m2crypto
Requires: python%{python3_pkgversion}-pyOpenSSL
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
%description -n python%{python3_pkgversion}-%{name}
The Python %{python3_version} client for SAML ECP authentication.
%endif

%package -n ciecp-utils
Summary: Command line utilities for SAML ECP authentication
%if 0%{?rhel} && 0%{?rhel} >= 8
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
%else
Requires: python2-%{name} = %{version}-%{release}
%endif
%description -n ciecp-utils
Command line utilities for SAML ECP authentication, including
ecp-cert-info, ecp-cookit-init, ecp-get-cert, and ecp-curl
(an ECP-aware curl alternative).

# -- build ------------------

%prep
%autosetup -n %{name}-%{version}

%build
# patch setup.py for old setuptools
%if 0%{?rhel} && 0%{?rhel} <= 7
# old setuptools does not support environment markers:
sed -i "/ ; /s/ ;.*/\",/g" setup.py
# remove winkerberos requirement
sed -i "/winkerberos/d" setup.py
%endif
# centos/epel provides kerberos (not pykerberos):
sed -i "s/pykerberos/kerberos/g" setup.py

# build python2
%py2_build

# build python3
%if 0%{?rhel} && 0%{?rhel} >= 8
%py3_build
%endif

%install
%py2_install
%if 0%{?rhel} && 0%{?rhel} >= 8
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

# -- files ------------------

%files -n python2-%{name}
%license LICENSE
%doc README.md
%{python2_sitelib}/*
%exclude %{python2_sitelib}/ciecplib/tool

%if 0%{?rhel} && 0%{?rhel} >= 8
%files -n python%{python3_pkgversion}-%{name}
%license LICENSE
%doc README.md
%{python3_sitelib}/*
%exclude %{python3_sitelib}/ciecplib/tool
%endif

%files -n ciecp-utils
%license LICENSE
%{_bindir}/*
%{_mandir}/man1/*.1*
%if 0%{?rhel} && 0%{?rhel} >= 8
%{python3_sitelib}/ciecplib/tool
%else
%{python2_sitelib}/ciecplib/tool
%endif

# -- changelog --------------

%changelog
* Wed Jan 22 2020 Duncan Macleod <duncan.macleod@ligo.org> - 0.1.0-1
- first release
