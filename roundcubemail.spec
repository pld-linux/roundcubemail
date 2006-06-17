# TODO:
# - prepare config for lighttp
# - add logrotate file
# - it has PEAR boundled inside - use system ones
# - use pear-deps system?
# - package: http://blog.ilohamail.org/ and remove boundled classess from it
#
%define		_beta	svn260
Summary:	RoundCube Webmail
Name:		roundcubemail
Version:	0.1
Release:	0.%{_beta}.0.2
License:	GPL v2
Group:		Applications/WWW
# Original source:
#Source0:	http://dl.sourceforge.net/roundcubemail/%{name}-%{version}%{_beta}.tar.gz
# Temporary place for svn-snapshot:
Source0:	http://www.blues.gda.pl/SOURCES/%{name}-%{version}%{_beta}.tar.bz2
# Source0-md5:	653777014b833e2bd08c875468fad7f2
Source1:	%{name}.config
Patch0:		%{name}-config.patch
URL:		http://www.roundcube.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-pcre
# Some php-database backend. Suggests?
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		roundcube
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_appdatadir	/var/lib/roundcube
%define		_applogdir	/var/log/roundcube

%description
RoundCube Webmail is a browser-based multilingual IMAP client with an
application-like user interface. It provides full functionality you
expect from an e-mail client, including MIME support, address book,
folder manipulation and message filters. RoundCube Webmail is written
in PHP and requires the MySQL database. The user interface is fully
skinnable using XHTML and CSS 2.

%prep
%setup -q -n %{name}-%{version}%{_beta}
%patch0 -p1

find -name .svn | xargs -r rm -rf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdatadir},%{_applogdir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_appdir}/{config,program,skins}

# Main application part:
cp -R program/* $RPM_BUILD_ROOT%{_appdir}/program
install index.php $RPM_BUILD_ROOT%{_appdir}

# Skins installation (maybe it should be as config??)
cp -R skins/* $RPM_BUILD_ROOT%{_appdir}/skins

## Configuration:
install config/db.inc.php.dist $RPM_BUILD_ROOT%{_sysconfdir}/db.inc.php
install config/main.inc.php.dist $RPM_BUILD_ROOT%{_sysconfdir}/main.inc.php
ln -sf %{_sysconfdir}/db.inc.php $RPM_BUILD_ROOT%{_appdir}/config/db.inc.php
ln -sf %{_sysconfdir}/main.inc.php $RPM_BUILD_ROOT%{_appdir}/config/main.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL README UPGRADING SQL
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%dir %{_appdir}
%{_appdir}/*.php
%dir %{_appdir}/config
%{_appdir}/config/*.php
%dir %{_appdir}/program
%{_appdir}/program/*
%dir %{_appdir}/skins
%{_appdir}/skins/default
%dir %attr(770,root,http) %{_applogdir}
%dir %attr(770,root,http) %{_appdatadir}
# %ghost logfile
