# TODO:
# - prepare config for lighttpd
# - it has PEAR boundled inside - use system ones
# - use pear-deps system?
# - use system js/tiny_mce
# - package: http://blog.ilohamail.org/ and remove boundled classess from it
#
#%define		_svn	837
#%define		_snap	20070927
%define		_beta	rc2
%define		_rel	0.1
Summary:	RoundCube Webmail
Summary(pl.UTF-8):	RoundCube Webmail - poczta przez WWW
Name:		roundcubemail
Version:	0.1
#Release:	5.%{_svn}.%{_rel}
Release:	6.%{_beta}.%{_rel}
License:	GPL v2
Group:		Applications/WWW
#Source0:	http://dl.sourceforge.net/roundcubemail/%{name}-nightly-%{_snap}.tar.gz
#Source0:	roundcubemail-%{_snap}.%{_svn}.tar.bz2
Source0:	http://dl.sourceforge.net/roundcubemail/%{name}-%{version}-%{_beta}.tar.gz
# Source0-md5:	a950ed7fff26e64fef20c2765b4890f7
Source1:	%{name}.config
Source2:	%{name}.logrotate
Patch0:		%{name}-config.patch
Patch1:		%{name}-faq-page.patch
Patch2:		%{name}-tz.patch
URL:		http://www.roundcube.net/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	%{name}-skin
Requires:	php(pcre)
# Some php-database backend. Suggests?
# php-sockets is required to make spellcheck working
Requires:	webapps
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

%package skin-default
Summary:	Default skin for RoundCube Webmail
Summary(pl.UTF-8):	Domyślna skórka dla RoundCube Webmaila
Group:		Applications/WWW
Provides:	%{name}-skin

%description skin-default
Default skin for RoundCube Webmail.

%description skin-default -l pl.UTF-8
Domyślna skórka dla RoundCube Webmaila.

%prep
%setup -q -n %{name}-%{version}-%{_beta}
%patch0 -p1
%patch1 -p1
%patch2 -p1

find -name .svn | xargs -r rm -rf

# undos the source
find '(' -name '*.php' -o -name '*.inc' -o -name '*.js' -o -name '*.css' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdatadir},%{_applogdir},%{_archivelogdir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{_appdir}/{bin,config,program,skins},/etc/logrotate.d}

# Main application part:
cp -a program/* $RPM_BUILD_ROOT%{_appdir}/program
cp -a bin/*.php $RPM_BUILD_ROOT%{_appdir}/bin
cp -a index.php $RPM_BUILD_ROOT%{_appdir}

# Skins installation
cp -a skins/* $RPM_BUILD_ROOT%{_appdir}/skins

## Configuration:
install config/db.inc.php.dist $RPM_BUILD_ROOT%{_sysconfdir}/db.inc.php
install config/main.inc.php.dist $RPM_BUILD_ROOT%{_sysconfdir}/main.inc.php
ln -sf %{_sysconfdir}/db.inc.php $RPM_BUILD_ROOT%{_appdir}/config/db.inc.php
ln -sf %{_sysconfdir}/main.inc.php $RPM_BUILD_ROOT%{_appdir}/config/main.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ ! -f %{_sysconfdir}/db.inc.php -o ! -f %{_sysconfdir}/main.inc.php ]; then
	# import configs from previously manually installed site
	d=/home/services/httpd/html/config
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

%post
if [ "$1" = 0 ]; then
%banner -e %{name} <<'EOF'
To customize installed languages set
 %%_install_langs in /etc/rpm/macros

EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL README UPGRADING SQL
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
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

%lang(am) %{_appdir}/program/localization/am
%lang(ar) %{_appdir}/program/localization/ar
%lang(bg) %{_appdir}/program/localization/bg
%lang(ca) %{_appdir}/program/localization/ca
%lang(cz) %{_appdir}/program/localization/cz
%lang(da) %{_appdir}/program/localization/da
%lang(de) %{_appdir}/program/localization/de_DE
%lang(de_CH) %{_appdir}/program/localization/de_CH
%lang(el) %{_appdir}/program/localization/el
%lang(en_GB) %{_appdir}/program/localization/en_GB
%lang(en_US) %{_appdir}/program/localization/en_US
%lang(eo) %{_appdir}/program/localization/eo
%lang(es) %{_appdir}/program/localization/es
%lang(et) %{_appdir}/program/localization/et_EE
%lang(eu) %{_appdir}/program/localization/eu
%lang(fa) %{_appdir}/program/localization/fa
%lang(fi) %{_appdir}/program/localization/fi
%lang(fr) %{_appdir}/program/localization/fr
%lang(ga_IE) %{_appdir}/program/localization/ga_IE
%lang(gl) %{_appdir}/program/localization/gl
%lang(hr) %{_appdir}/program/localization/hr
%lang(hu) %{_appdir}/program/localization/hu
%lang(it) %{_appdir}/program/localization/it
%lang(ja) %{_appdir}/program/localization/ja
%lang(lt) %{_appdir}/program/localization/lt
%lang(lv) %{_appdir}/program/localization/lv
%lang(mk) %{_appdir}/program/localization/mk
%lang(ms_MY) %{_appdir}/program/localization/ms_MY
%lang(nb) %{_appdir}/program/localization/nb_NO
%lang(nl) %{_appdir}/program/localization/nl_NL
%lang(pl) %{_appdir}/program/localization/pl
%lang(pt) %{_appdir}/program/localization/pt_PT
%lang(pt_BR) %{_appdir}/program/localization/pt_BR
%lang(ro) %{_appdir}/program/localization/ro
%lang(ru) %{_appdir}/program/localization/ru
%lang(se) %{_appdir}/program/localization/se
%lang(si) %{_appdir}/program/localization/si
%lang(sk) %{_appdir}/program/localization/sk
%lang(sl) %{_appdir}/program/localization/sl
%lang(tr) %{_appdir}/program/localization/tr
%lang(uk) %{_appdir}/program/localization/uk
%lang(zh_CN) %{_appdir}/program/localization/zh_CN
%lang(zh_TW) %{_appdir}/program/localization/zh_TW

%dir %{_appdir}/skins
%dir %attr(770,root,http) %{_applogdir}
%dir %attr(751,root,logs) %{_archivelogdir}
%dir %attr(770,root,http) %{_appdatadir}
# %ghost logfile

%files skin-default
%defattr(644,root,root,755)
%{_appdir}/skins/default
