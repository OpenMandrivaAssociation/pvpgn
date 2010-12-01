%define _disable_ld_no_undefined 1

Name: pvpgn
Version: 199.r577
Release: %mkrel 1
Summary: PvPGN is a BNETD mod which aims to provide support for all Blizzard clients
License: GPLv2
Group: Games/Other
Url: http://pvpgn.berlios.de
Source: http://download.berlios.de/pvpgn/%{name}-%{version}.tar.bz2
Source1: %{name}.init
Source2: %{name}.logrotate
Patch1: DefineInstallationPaths.cmake.patch
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildRequires: MySQL-devel libpcap-devel libsqlite3-devel zlib-devel

%description
PvPGN is a BNETD mod which aims to provide support for all Blizzard clients (thus it supports all BNETD supported clients plus the most recent ones).
The list of supported clients and their minimum verion required is:
- Diablo 1 v1.09
- Starcraft v1.08
- BroodWar v1.08
- Warcraft II Battle.Net Edition v2.05
- Diablo 2 v1.10 (*)
- Diablo 2 LOD v1.10
- Warcraft III Reign Of Chao
- Warcraft III Frozen Throne

This build of PvPGN is linked with MySQL and SQLite3 libraries.

%prep
%setup -q
%patch1 -p0

%build
%cmake -DAPPLICATION_NAME=pvpgn -DWITH_MYSQL=true
%make

%install
rm -fr %{buildroot}
%makeinstall_std -C build
install -d -m755 %{buildroot}/etc/pvpgn
install -d -m755 %{buildroot}/etc/rc.d/init.d
install -d -m755 %{buildroot}/var/log/pvpgn
install -d -m750 %{buildroot}/etc/logrotate.d
install -m755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/pvpgn
install -m640 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/pvpgn
mkdir -p -m755 %{buildroot}/var/run/%{name}

%clean
rm -fr %{buildroot}

%pre
%{_sbindir}/groupadd -r -f pvpgn 2>/dev/null ||:
%{_sbindir}/useradd -g pvpgn -c 'PvPGN' -d /dev/null -s '' -r pvpgn 2>/dev/null ||:

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/*
%doc docs/* version-history.txt TODO README CREDITS COPYING BUGS README.DEV
%{_bindir}/*
%{_sbindir}/*
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%{_mandir}/*
/var/lib/%{name}/*
%attr(750,pvpgn,pvpgn) %dir %{_logdir}/%{name}
%attr(750,pvpgn,pvpgn) %dir /var/run/%{name}
%attr(750,pvpgn,pvpgn) %dir /var/lib/%{name}
