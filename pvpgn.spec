%define support_version 1.3

Name: pvpgn
Version: 199.r577
Release: %mkrel 2
Summary: PvPGN is a BNETD mod which aims to provide support for all Blizzard clients
License: GPLv2
Group: Games/Other
Url: http://pvpgn.berlios.de
Source: http://download.berlios.de/pvpgn/%{name}-%{version}.tar.bz2
Source2: http://download.berlios.de/pvpgn/%{name}-support-%{support_version}.tar.gz
Source3: %{name}.init
Source4: %{name}.logrotate
Patch1: DefineInstallationPaths.cmake.patch
Patch2: pvpgn-fix-bnet-deletion.patch
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildRequires: MySQL-devel libpcap-devel libsqlite3-devel zlib-devel
BuildRequires: cmake

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

%package support
Requires: pvpgn
Group: Games/Other
Summary: PvPGN is a BNETD mod which aims to provide support for all Blizzard clients

%description support
These are the support files required for PvPGN


%prep
%setup -q
tar xzf %{SOURCE2}
%patch1 -p0
%patch2 -p0

%build
cmake -DAPPLICATION_NAME=pvpgn -DWITH_MYSQL=true \
-D CMAKE_INSTALL_PREFIX=/usr \
-D EXEC_INSTALL_PREFIX=/usr ./

%make

%install
rm -fr %{buildroot}
%makeinstall_std
install -d -m755 %{buildroot}/etc/pvpgn
install -d -m755 %{buildroot}/etc/rc.d/init.d
install -d -m755 %{buildroot}/var/log/pvpgn
install -d -m750 %{buildroot}/etc/logrotate.d
install -m755 %{SOURCE2} %{buildroot}%{_sysconfdir}/rc.d/init.d/pvpgn
install -m640 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/pvpgn
mkdir -p -m755 %{buildroot}/var/run/%{name}

# support files
mkdir -p %{buildroot}%{_var}/lib/pvpgn/files/
cp -r %{name}-support-%{support_version} %{buildroot}%{_var}/lib/pvpgn/files/

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

%files support
%defattr(-,root,root)
%{_var}/lib/%{name}/*
