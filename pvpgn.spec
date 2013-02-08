%define support_version 1.3

Name: pvpgn
Version: 199.r577
Release: 6
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
Patch3: pvpgn-build-static-lib.patch
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildRequires: mysql-devel libpcap-devel zlib-devel
BuildRequires: cmake

%description
PvPGN is a BNETD mod which aims to provide support for all Blizzard clients
(thus it supports all BNETD supported clients plus the most recent ones).
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
tar xzf %{SOURCE2}
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
%cmake -DWITH_MYSQL=ON
%make

%install
%makeinstall_std -C build
install -d -m755 %{buildroot}/etc/pvpgn
install -d -m755 %{buildroot}/etc/rc.d/init.d
install -d -m755 %{buildroot}/var/log/pvpgn
install -d -m750 %{buildroot}/etc/logrotate.d
install -m755 %{SOURCE3} %{buildroot}%{_sysconfdir}/rc.d/init.d/pvpgn
install -m640 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/pvpgn
mkdir -p -m755 %{buildroot}/var/run/%{name}

# support files
mkdir -p %{buildroot}%{_var}/lib/pvpgn/files/
cp -r %{name}-support-%{support_version}/* %{buildroot}%{_var}/lib/pvpgn/files/

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


%changelog
* Mon Mar 21 2011 Funda Wang <fwang@mandriva.org> 199.r577-5mdv2011.0
+ Revision: 647324
- fix build with default cmake build options

  + zamir <zamir@mandriva.org>
    - fix deps
    - fix locate support files
    - fix spec and init file
    - fix logrotate file

  + Oden Eriksson <oeriksson@mandriva.com>
    - relink against libmysqlclient.so.18

* Thu Dec 02 2010 Eugeni Dodonov <eugeni@mandriva.com> 199.r577-1mdv2011.0
+ Revision: 604720
- Add pvpgn-support files.
- Add URL for pvpgn-support
- Add BR for cmake.
  Build pvpgn-support as well.
- Fix build.
- Use %%cmake macro

  + zamir <zamir@mandriva.org>
    - small fix build
    - first build
    - Created package structure for pvpgn.

