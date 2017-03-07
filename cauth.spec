%global  sum Python-based SSO server used by the Software Factory project

Name:    cauth
Version: 0.7.1.dev24
Release: 0.source.0.7.0.24.g7b2fb1b.distgit.1%{?dist}
Summary: %{sum}

License: ASL 2.0
URL:            https://softwarefactory-project.io/r/p/%{name}
Source0: HEAD.tgz

BuildArch: noarch

BuildRequires: m2crypto
BuildRequires: python-sqlalchemy
BuildRequires: python-basicauth
BuildRequires: python-flake8
BuildRequires: python-nose
BuildRequires: python-setuptools
BuildRequires: python-webtest
BuildRequires: python2-mockldap
BuildRequires: python2-oic
BuildRequires: python2-pygerrit
BuildRequires: python2-devel
BuildRequires: python2-future
BuildRequires: python2-httmock
BuildRequires: python2-keystoneclient
BuildRequires: python2-mock
BuildRequires: python2-pbr
BuildRequires: python2-pecan

%description
%{sum}

%package -n python2-%{name}
Summary: %{sum}

Requires: MySQL-python
Requires: m2crypto
Requires: python-basicauth
Requires: python-sphinx
Requires: python-sqlalchemy
Requires: python2-oic
Requires: python2-pbr
Requires: python2-pecan
Requires: python2-pygerrit
Requires: python2-redmine
Requires: python2-requests
Requires: python2-stevedore
Requires: python2-wsgiref

%description -n python2-%{name}
%{sum}

%prep
%autosetup -n %{name}-%{version}

%build
export PBR_VERSION=%{version}
%{__python2} setup.py build

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install --skip-build --root %{buildroot}

%check
PYTHONPATH=%{buildroot}/%{python2_sitelib} PBR_VERSION=%{version} nosetests -v

%files -n python2-%{name}
%{python2_sitelib}/*

%changelog
* Mon Mar 6 2017 Nicolas Hicher <nhicher@redhat.com> 1.0.0-1
- Initial packaging
