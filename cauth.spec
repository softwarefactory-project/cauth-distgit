%global  sum Python-based SSO server used by the Software Factory project

Name:    cauth
Version: 0.7.1
Release: 2%{?dist}
Summary: %{sum}

License: ASL 2.0
URL:     https://softwarefactory-project.io/r/p/%{name}
Source0: https://github.com/redhat-cip/%{name}/archive/%{version}.tar.gz
Source1: cauth_logrotate.conf

BuildArch: noarch

BuildRequires: MySQL-python
BuildRequires: m2crypto
BuildRequires: python-sqlalchemy
BuildRequires: python-flake8
BuildRequires: python-nose
BuildRequires: python-setuptools
BuildRequires: python-webtest
BuildRequires: python2-basicauth
BuildRequires: python2-cryptodomex
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
Requires: httpd
Requires: m2crypto
Requires: mod_auth_pubtkt
Requires: python-sphinx
Requires: python-sqlalchemy
Requires: python2-basicauth
Requires: python2-oic
Requires: python2-pbr
Requires: python2-pecan
Requires: python2-pygerrit
Requires: python2-redmine
Requires: python2-requests
Requires: python2-stevedore
Requires: python2-wsgiref
Requires: policycoreutils

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
install -d %{buildroot}/%{_var}/www/%{name}
install -d %{buildroot}/%{_var}/log/%{name}
install -d %{buildroot}/%{_var}/lib/%{name}/{templates,keys}
install -d %{buildroot}/%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/logrotate.d/cauth.conf
install -p -D -m 640 etc/config.py %{buildroot}%{_sysconfdir}/%{name}/config.py
rm etc/config.py{c,o}

%check
PYTHONPATH=%{buildroot}/%{python2_sitelib} PBR_VERSION=%{version} nosetests -v

%pre
getent group cauth >/dev/null || groupadd -r cauth
if ! getent passwd cauth >/dev/null; then
    useradd -r -g cauth -G cauth -d %{_sharedstatedir}/cauth -s /sbin/nologin -c "Cauth Daemon" cauth
fi
exit 0

%post
semanage fcontext -a -t httpd_sys_content_t %{buildroot}/%{_sysconfdir}/%{name}
semanage fcontext -a -t httpd_sys_content_t %{buildroot}/%{_var}/www/%{name}
restorecon -rv  %{buildroot}/%{_sysconfdir}/%{name}
restorecon -rv  %{buildroot}/%{_var}/www/%{name}

%files -n python2-%{name}
%doc LICENSE
%{python2_sitelib}/*
%attr(0750, apache, apache) %{_var}/lib/%{name}
%attr(0750, apache, apache) %{_var}/log/%{name}
%attr(0750, apache, apache) %{_var}/www/%{name}
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/logrotate.d/cauth.conf
%config(noreplace) %attr(0640, root, cauth) %{_sysconfdir}/cauth/config.py

%changelog
* Mon Mar 6 2017 Nicolas Hicher <nhicher@redhat.com> 0.7.1-2
- Create directories in packages
- Add logrotate config file

* Mon Mar 6 2017 Nicolas Hicher <nhicher@redhat.com> 0.7.1-1
- Initial packaging
