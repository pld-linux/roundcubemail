# TODO:
# - prepare config for lighttpd
# - it has PEAR boundled inside - use system ones
# - use pear-deps system?
# - use system js/tiny_mce
# - package: http://blog.ilohamail.org/ and remove boundled classess from it
# - Some php-database backend. Suggests?
# - test/finish and then enable by default password-anon-ldap-bind patch
#
%bcond_with	spamfilter	# Build with spamfilter patch
%bcond_with	postfixadmin	# Build with postfixadmin support patch
%bcond_with	password_anon_ldap_bind	# apply with password-anon-ldap-bind patch.

%define		rcpfa_ver	1.0.5
Summary:	RoundCube Webmail
Summary(pl.UTF-8):	RoundCube Webmail - poczta przez WWW
Name:		roundcubemail
Version:	0.3.1
Release:	2
License:	GPL v2
Group:		Applications/Mail
Source0:	http://downloads.sourceforge.net/roundcubemail/%{name}-%{version}.tar.gz
# Source0-md5:	34e8e18772e7eada8769b6c5c20f7c8e
Source1:	%{name}.config
Source2:	%{name}.logrotate
Source3:	%{name}-lighttpd.conf
Source4:	http://nejc.skoberne.net/wp-content/uploads/2008/11/rcpfa-105.tgz
# Source4-md5:	dc23bcd894f693db74fce53b09ab58d6
Patch0:		%{name}-config.patch
Patch1:		%{name}-spam.patch
Patch2:		%{name}-postfixadmin-pl_locales.patch
Patch3:		%{name}-faq-page.patch
Patch4:		%{name}-password-anon-ldap-bind.patch
URL:		http://www.roundcube.net/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	%{name}-skin
Requires:	php(dom)
Requires:	php(imap)
Requires:	php(pcre)
Requires:	php(session)
Requires:	php(sockets)
Requires:	php(spl)
Requires:	php(xml)
Requires:	php-pear-DB
Requires:	rpm-whiteout >= 1.22
Requires:	webapps
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Suggests:	php(gd)
Suggests:	php(iconv)
Suggests:	php(mbstring)
Suggests:	php(mcrypt)
Suggests:	php(openssl)
Suggests:	php-pear-Net_LDAP2
Suggests:	php-pecl-fileinfo
Conflicts:	logrotate < 3.7-4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		roundcube
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_appdatadir	/var/lib/roundcube
%define		_applogdir	/var/log/roundcube
%define		_archivelogdir	/var/log/archive/roundcube

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

%package skin-default
Summary:	Default skin for RoundCube Webmail
Summary(pl.UTF-8):	Domyślna skórka dla RoundCube Webmaila
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-skin

%description skin-default
Default skin for RoundCube Webmail.

%description skin-default -l pl.UTF-8
Domyślna skórka dla RoundCube Webmaila.

%prep
%setup -q %{?with_postfixadmin:-a 4}
%patch0 -p1
%if %{with spamfilter}
%patch1 -p1
%endif
%if %{with postfixadmin}
#patch2 -p1
%endif
%patch3 -p1
%if %{with password_anon_ldap_bind}
%patch4 -p1
%endif

find -name .svn | xargs -r rm -rf

# undos the source
find '(' -name '*.php' -o -name '*.inc' -o -name '*.js' -o -name '*.css' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

mv config/db.inc.php.dist config/db.inc.php
mv config/main.inc.php.dist config/main.inc.php
%if %{with postfixadmin}
mv rcpfa-%{rcpfa_ver} rcpfa
cd rcpfa
cp code/forwarding.html ../skins/default/templates
cp code/password.html ../skins/default/templates
cp code/vacation.html ../skins/default/templates
cp code/pfa_forwarding.inc ../program/steps/settings
cp code/pfa_password.inc ../program/steps/settings
cp code/pfa_vacation.inc ../program/steps/settings
cp code/pfa.php ../program/include

patch -d .. -p1 < diffs/app.js.diff
patch -d .. -p1 < diffs/db.inc.php.diff
patch -d .. -p1 < diffs/func.inc.diff
patch -d .. -p1 < diffs/index.php.diff
patch -d .. -p1 < diffs/labels.inc.diff
patch -d .. -p1 < diffs/main.inc.diff
patch -d .. -p1 < diffs/main.inc.php.diff
patch -d .. -p1 < diffs/messages.inc.diff
patch -d .. -p1 < diffs/rcube_user.php.diff
patch -d .. -p1 < diffs/settingstabs.html.diff
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdatadir},%{_applogdir},%{_archivelogdir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{_appdir}/{bin,config,installer,program,skins},/etc/logrotate.d}

# Main application part:
cp -a program/* $RPM_BUILD_ROOT%{_appdir}/program
cp -a bin/*.php $RPM_BUILD_ROOT%{_appdir}/bin
cp -a index.php $RPM_BUILD_ROOT%{_appdir}

# Skins installation
cp -a skins/* $RPM_BUILD_ROOT%{_appdir}/skins

# Installer part
cp -a installer/* $RPM_BUILD_ROOT%{_appdir}/installer
cp -a config/db.inc.php $RPM_BUILD_ROOT%{_appdir}/config/db.inc.php.dist
cp -a config/main.inc.php $RPM_BUILD_ROOT%{_appdir}/config/main.inc.php.dist
cp -a SQL $RPM_BUILD_ROOT%{_appdir}

# Plugins
cp -a plugins $RPM_BUILD_ROOT%{_appdir}/plugins

## Configuration:
cp -a config/db.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/db.inc.php
cp -a config/main.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/main.inc.php
ln -sf %{_sysconfdir}/db.inc.php $RPM_BUILD_ROOT%{_appdir}/config/db.inc.php
ln -sf %{_sysconfdir}/main.inc.php $RPM_BUILD_ROOT%{_appdir}/config/main.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ ! -f %{_sysconfdir}/db.inc.php -o ! -f %{_sysconfdir}/main.inc.php ]; then
	# import configs from previously manually installed site
	d=/home/services/httpd/html/config
	if [ -f $d/db.inc.php -o -f $d/main.inc.php ]; then
		echo >&2 "Importing site configs from $d"
		mkdir -p %{_sysconfdir}
		if [ -f $d/db.inc.php ]; then
			[ -f %{_sysconfdir}/db.inc.php ] && mv -f %{_sysconfdir}/db.inc.php{,.rpmorig}
			cp -af $d/db.inc.php %{_sysconfdir}/db.inc.php
		fi
		if [ -f $d/main.inc.php ]; then
			[ -f %{_sysconfdir}/main.inc.php ] && mv -f %{_sysconfdir}/main.inc.php{,.rpmorig}
			cp -af $d/main.inc.php %{_sysconfdir}/main.inc.php
		fi
	fi
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL README UPGRADING
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%dir %{_appdir}
%{_appdir}/*.php
%dir %{_appdir}/bin
%{_appdir}/bin/*.php
%dir %{_appdir}/config
%{_appdir}/config/*.php
%dir %{_appdir}/program
%{_appdir}/program/*.gif
%{_appdir}/program/include
%{_appdir}/program/js
%{_appdir}/program/lib
%{_appdir}/program/steps
%dir %{_appdir}/program/localization
%{_appdir}/program/localization/index.inc
%{_appdir}/plugins

%lang(ar_SA) %{_appdir}/program/localization/ar_SA
%lang(ast) %{_appdir}/program/localization/ast
%lang(az) %{_appdir}/program/localization/az_AZ
%lang(bg) %{_appdir}/program/localization/bg_BG
%lang(bn_BD) %{_appdir}/program/localization/bn_BD
%lang(br) %{_appdir}/program/localization/br
%lang(bs) %{_appdir}/program/localization/bs_BA
%lang(ca) %{_appdir}/program/localization/ca_ES
%lang(cs) %{_appdir}/program/localization/cs_CZ
%lang(cy) %{_appdir}/program/localization/cy_GB
%lang(da) %{_appdir}/program/localization/da_DK
%lang(de) %{_appdir}/program/localization/de_DE
%lang(de_CH) %{_appdir}/program/localization/de_CH
%lang(el) %{_appdir}/program/localization/el_GR
%lang(en_GB) %{_appdir}/program/localization/en_GB
%lang(en_US) %{_appdir}/program/localization/en_US
%lang(eo) %{_appdir}/program/localization/eo
%lang(es) %{_appdir}/program/localization/es_ES
%lang(es_AR) %{_appdir}/program/localization/es_AR
%lang(et) %{_appdir}/program/localization/et_EE
%lang(eu) %{_appdir}/program/localization/eu_ES
%lang(fa) %{_appdir}/program/localization/fa
%lang(fa_AF) %{_appdir}/program/localization/fa_AF
%lang(fi) %{_appdir}/program/localization/fi_FI
%lang(fr) %{_appdir}/program/localization/fr_FR
%lang(ga) %{_appdir}/program/localization/ga_IE
%lang(gl) %{_appdir}/program/localization/gl_ES
%lang(he) %{_appdir}/program/localization/he_IL
%lang(hi) %{_appdir}/program/localization/hi_IN
%lang(hr) %{_appdir}/program/localization/hr_HR
%lang(hu) %{_appdir}/program/localization/hu_HU
%lang(hy) %{_appdir}/program/localization/hy_AM
%lang(id) %{_appdir}/program/localization/id_ID
%lang(is) %{_appdir}/program/localization/is_IS
%lang(it) %{_appdir}/program/localization/it_IT
%lang(ja) %{_appdir}/program/localization/ja_JP
%lang(ka) %{_appdir}/program/localization/ka_GE
%lang(ko) %{_appdir}/program/localization/ko_KR
%lang(ku) %{_appdir}/program/localization/ku
%lang(lt) %{_appdir}/program/localization/lt_LT
%lang(lv) %{_appdir}/program/localization/lv_LV
%lang(mk) %{_appdir}/program/localization/mk_MK
%lang(mr) %{_appdir}/program/localization/mr_IN
%lang(ms) %{_appdir}/program/localization/ms_MY
%lang(nb) %{_appdir}/program/localization/nb_NO
%lang(ne) %{_appdir}/program/localization/ne_NP
%lang(nl) %{_appdir}/program/localization/nl_NL
%lang(nl_BE) %{_appdir}/program/localization/nl_BE
%lang(nn) %{_appdir}/program/localization/nn_NO
%lang(pl) %{_appdir}/program/localization/pl_PL
%lang(ps) %{_appdir}/program/localization/ps
%lang(pt) %{_appdir}/program/localization/pt_PT
%lang(pt_BR) %{_appdir}/program/localization/pt_BR
%lang(ro) %{_appdir}/program/localization/ro_RO
%lang(ru) %{_appdir}/program/localization/ru_RU
%lang(si) %{_appdir}/program/localization/si_LK
%lang(sk) %{_appdir}/program/localization/sk_SK
%lang(sl) %{_appdir}/program/localization/sl_SI
%lang(sq) %{_appdir}/program/localization/sq_AL
%lang(sr) %{_appdir}/program/localization/sr_CS
%lang(sv) %{_appdir}/program/localization/sv_SE
%lang(th) %{_appdir}/program/localization/th_TH
%lang(tr) %{_appdir}/program/localization/tr_TR
%lang(uk) %{_appdir}/program/localization/uk_UA
%lang(vn) %{_appdir}/program/localization/vi_VN
%lang(zh_CN) %{_appdir}/program/localization/zh_CN
%lang(zh_TW) %{_appdir}/program/localization/zh_TW

%dir %{_appdir}/skins
%dir %attr(770,root,http) %{_applogdir}
%dir %attr(751,root,logs) %{_archivelogdir}
%dir %attr(770,root,http) %{_appdatadir}

# TODO: %ghost logfile(s)

%files setup
%defattr(644,root,root,755)
%dir %{_appdir}/installer
%{_appdir}/installer/*.php
%{_appdir}/installer/client.js
%{_appdir}/installer/styles.css
%{_appdir}/installer/welcome.html
%{_appdir}/installer/images
%{_appdir}/config/*.php.dist
%{_appdir}/SQL

%files skin-default
%defattr(644,root,root,755)
%{_appdir}/skins/default
