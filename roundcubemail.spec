# TODO:
# - use system js/tiny_mce
# - use system js/jquery
# - package: http://blog.ilohamail.org/ and remove boundled classess from it
# - test/finish and then enable by default password-anon-ldap-bind patch
# - bconds does not work for a long time
#
%bcond_with	spamfilter	# Build with spamfilter patch
%bcond_with	postfixadmin	# Build with postfixadmin support patch
%bcond_with	password_anon_ldap_bind	# apply with password-anon-ldap-bind patch.

%define		rcpfa_ver	1.0.5
%define		php_min_version 5.3.7
%include	/usr/lib/rpm/macros.php
Summary:	RoundCube Webmail
Summary(pl.UTF-8):	RoundCube Webmail - poczta przez WWW
Name:		roundcubemail
Version:	1.0.12
Release:	2
License:	GPL v3+
Group:		Applications/Mail
Source0:	https://github.com/roundcube/%{name}/releases/download/%{version}/%{name}-%{version}-dep.tar.gz
# Source0-md5:	675b86f5ad2b67ac064a981d79ac3172
Source1:	apache.conf
Source2:	%{name}.logrotate
Source3:	lighttpd.conf
Source4:	http://nejc.skoberne.net/wp-content/uploads/2008/11/rcpfa-105.tgz
# Source4-md5:	dc23bcd894f693db74fce53b09ab58d6
Source5:	find-lang.sh
Source6:	httpd.conf
Patch0:		%{name}-config.patch
Patch1:		%{name}-spam.patch
Patch2:		%{name}-postfixadmin-pl_locales.patch
Patch3:		%{name}-faq-page.patch
Patch4:		%{name}-password-anon-ldap-bind.patch
URL:		http://www.roundcube.net/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	sed >= 4.0
Requires:	%{name}-skin
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(dom)
Requires:	php(filter)
Requires:	php(iconv)
Requires:	php(imap)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(mcrypt)
Requires:	php(pcre)
Requires:	php(pdo)
Requires:	php(session)
Requires:	php(simplexml)
Requires:	php(sockets)
Requires:	php(spl)
Requires:	php(xml)
Requires:	php-pear-DB
Requires:	php-pear-Mail_Mime >= 1.8.1
Requires:	php-pear-Net_IDNA2 >= 0.1.1
Requires:	php-pear-Net_SMTP
Requires:	rpm-whiteout >= 1.22
Requires:	webapps
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Requires(post):	openssl-tools
Suggests:	php(exif)
Suggests:	php(fileinfo)
Suggests:	php(gd)
Suggests:	php(intl)
Suggests:	php(openssl)
Suggests:	php(xml)
Suggests:	php(zip)
Suggests:	php-pear-Auth_SASL >= 1.0.6
# at least one pdo db driver needed
Suggests:	php(pdo-pgsql)
Suggests:	php(pdo-mysql)
Suggests:	php(pdo-sqlite)
Suggests:	php-pear-Crypt_GPG >= 1.2.0
Suggests:	php-pear-Net_LDAP2
Suggests:	php-pear-Net_Sieve >= 1.3.2
Suggests:	php-pear-Net_Socket
Obsoletes:	roundcube-plugin-jqueryui
Obsoletes:	roundcubemail-skin-default
Conflicts:	apache-base < 2.4.0-1
Conflicts:	logrotate < 3.8.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		roundcube
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_appdatadir	/var/lib/roundcube
%define		_applogdir	/var/log/roundcube
%define		_archivelogdir	/var/log/archive/roundcube

%define		find_lang 	sh %{SOURCE5} %{buildroot}

%define		_noautoreq_pear	.*

# exclude optional php dependencies
%define		_noautophp	php-sqlite php-mysql php-mysqli php-pgsql php-hash php-json php-xml

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp}

%description
RoundCube Webmail is a browser-based multilingual IMAP client with an
application-like user interface. It provides full functionality you
expect from an e-mail client, including MIME support, address book,
folder manipulation and message filters. RoundCube Webmail is written
in PHP and requires the MySQL database. The user interface is fully
skinnable using XHTML and CSS 2.

%description -l pl.UTF-8
RoundCube Webmail to oparty na przeglądarce wielojęzyczny klient PHP z
interfejsem użytkownika podobnym do aplikacji. Udostępnia pełną
funkcjonalność jakiej można oczekiwać od klienta pocztowego, w tym
obsługę MIME, książkę adresową, operacje na folderach i filtry
wiadomości. RoundCube Webmail jest napisany w PHP i wymaga bazy danych
MySQL. Interfejs użytkownika można w pełni obudować skórką przy użyciu
XHTML-a i CSS 2.

%package setup
Summary:	Installer script for RoundCube Webmail
Summary(pl.UTF-8):	Skrypt instalacyjny RoundCube Webmaila
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
This package provides installer script for RoundCube Webmail.

%description setup -l pl.UTF-8
Ten pakiet zawiera skrypt instalacyjny RoundCube Webmaila.

%package skin-classic
Summary:	Classic skin for RoundCube Webmail
Summary(pl.UTF-8):	Klasyczna skórka dla RoundCube Webmaila
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-skin

%description skin-classic
Classic skin for RoundCube Webmail.

%description skin-classic -l pl.UTF-8
Klasyczna skórka dla RoundCube Webmaila.

%package skin-larry
Summary:	Larry skin for RoundCube Webmail
Summary(pl.UTF-8):	Skórka Larry dla RoundCube Webmaila
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-skin

%description skin-larry
Larry skin for RoundCube Webmail.

%description skin-larry -l pl.UTF-8
Skórka Larry dla RoundCube Webmaila.

%prep
%setup -q -n %{name}-%{version}-dep %{?with_postfixadmin:-a 4}
%patch0 -p1
%if %{with spamfilter}
%patch1 -p1
%endif
%if %{with postfixadmin}
#patch2 -p1
%endif
#%patch3 -p1
%if %{with password_anon_ldap_bind}
%patch4 -p1
%endif

find -name .svn | xargs -r rm -rf

# undos the source
%undos -f php,inc,js,css

# fill proper shebang
%{__sed} -i -e '1s,^#!.*php,#!/usr/bin/php,' bin/*.sh
# these are php scripts really
for a in $(grep -l '<?php' bin/*.sh); do
	mv $a ${a%.sh}
done
%{__sed} -i s/indexcontacts.sh/indexcontacts/g bin/update
%{__sed} -i s/updatedb.sh/updatedb/g bin/update

# tools to pack js
rm bin/jsshrink.sh
rm bin/cssshrink.sh

# pear package junk
rm -v plugins/*/package.xml

mv config/config.inc.php{.sample,}

%if %{with postfixadmin}
mv rcpfa-%{rcpfa_ver} rcpfa
cd rcpfa
cp -p code/forwarding.html ../skins/default/templates
cp -p code/password.html ../skins/default/templates
cp -p code/vacation.html ../skins/default/templates
cp -p code/pfa_forwarding.inc ../program/steps/settings
cp -p code/pfa_password.inc ../program/steps/settings
cp -p code/pfa_vacation.inc ../program/steps/settings
cp -p code/pfa.php ../program/include

%{__patch} -d .. -p1 < diffs/app.js.diff
%{__patch} -d .. -p1 < diffs/db.inc.php.diff
%{__patch} -d .. -p1 < diffs/func.inc.diff
%{__patch} -d .. -p1 < diffs/index.php.diff
%{__patch} -d .. -p1 < diffs/labels.inc.diff
%{__patch} -d .. -p1 < diffs/main.inc.diff
%{__patch} -d .. -p1 < diffs/config.inc.php.diff
%{__patch} -d .. -p1 < diffs/messages.inc.diff
%{__patch} -d .. -p1 < diffs/rcube_user.php.diff
%{__patch} -d .. -p1 < diffs/settingstabs.html.diff
%endif

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdatadir},%{_applogdir},%{_archivelogdir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{_appdir}/{bin,config,installer,program,skins},/etc/logrotate.d}

# Main application part:
cp -a program/* $RPM_BUILD_ROOT%{_appdir}/program
cp -a bin/* $RPM_BUILD_ROOT%{_appdir}/bin
cp -a index.php $RPM_BUILD_ROOT%{_appdir}

# Skins installation
cp -a skins/* $RPM_BUILD_ROOT%{_appdir}/skins

# Installer part
cp -a installer/* $RPM_BUILD_ROOT%{_appdir}/installer
cp -a SQL $RPM_BUILD_ROOT%{_appdir}

# Plugins
cp -a plugins $RPM_BUILD_ROOT%{_appdir}/plugins

## Configuration:
for a in config/*.php; do
	cp -p $a $RPM_BUILD_ROOT%{_sysconfdir}
	ln -s %{_sysconfdir}/$(basename $a) $RPM_BUILD_ROOT%{_appdir}/config
done
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

# find locales
%find_lang %{name}.lang
# sed -ne 's/%lang(\([^)]\+\).*/\1/p' %{name}.lang | sort -u | grep _

# now package plugins using filelist as well, as due lang tagging the files
# section will go unmanageable
for p in $RPM_BUILD_ROOT%{_appdir}/plugins/*; do
	echo "%dir ${p#$RPM_BUILD_ROOT}"
	for p in $p/*; do
		d=${p##*/}
		p=${p#$RPM_BUILD_ROOT}
		case "$d" in
		localization)
			continue
			;;
		README | Changelog | composer.json | config.inc.php.dist)
			echo "%doc $p"
			;;
		*)
			echo "$p"
			;;
		esac
	done
done > plugins.lang
cat plugins.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# replace default des string in config file for better security
makedesstr() {
	openssl rand -hex 12
}

if grep -q '24ByteDESkey' %{_sysconfdir}/config.inc.php; then
	des=$(makedesstr)
	# precaution if random str generation failed
	if [ c$(echo -n "$des" | wc -c) = c24 ]; then
		%{__sed} -i -e "s/rcmail-\!24ByteDESkey\*Str/$des/" %{_sysconfdir}/config.inc.php
	fi
fi

# Note this on version upgrade
%triggerpostun -- %{name} < %{version}-0
# don't do anything on --downgrade
if [ $1 -le 1 ]; then
	exit 0
fi
%banner -e %{name}-upgrade <<-EOF
Run %{_appdir}/bin/update to update to version %{version}.
(Be sure to have %{name}-setup installed when you run it)

See %{_docdir}/%{name}-%{version}/UPGRADING* for more information.
EOF

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL README.md UPGRADING
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.inc.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/defaults.inc.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mimetypes.php
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%dir %{_appdir}/program
%{_appdir}/program/include
%{_appdir}/program/js
%{_appdir}/program/lib
%{_appdir}/program/resources
%{_appdir}/program/steps
%{_appdir}/program/localization/index.inc

%dir %{_appdir}/plugins

%dir %{_appdir}/skins
%dir %attr(770,root,http) %{_applogdir}
%dir %attr(751,root,logs) %{_archivelogdir}
%dir %attr(770,root,http) %{_appdatadir}

# TODO: %ghost logfile(s)

%files setup
%defattr(644,root,root,755)
%dir %{_appdir}/bin
%attr(755,root,root) %{_appdir}/bin/*
%dir %{_appdir}/installer
%{_appdir}/installer/*.php
%{_appdir}/installer/client.js
%{_appdir}/installer/styles.css
%{_appdir}/installer/images
%{_appdir}/SQL

%files skin-classic
%defattr(644,root,root,755)
%{_appdir}/skins/classic

%files skin-larry
%defattr(644,root,root,755)
%{_appdir}/skins/larry
