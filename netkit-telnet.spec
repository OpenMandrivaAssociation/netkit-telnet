Summary:	Client for the telnet remote login protocol
Name:		netkit-telnet
Version:	0.17
Release:	%mkrel 1
License:	BSD
Group:		Networking/Remote access
URL:		ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/
Source0:	ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-telnet-%{version}.tar.bz2
Source2:	telnet-client.tar
Patch0:		telnet-client-cvs.patch
Patch1:		telnetd-0.17.diff
Patch2:		telnet-0.17-env.patch
Patch3:		telnet-0.17-pek.patch
Patch4:		telnet-0.17-issue.patch
Patch5:		telnet-0.17-sa-01-49.patch
Patch6:		telnet-0.17-8bit.patch
Patch7:		telnet-0.17-argv.patch
Patch8:		telnet-0.17-conf.patch
Patch9:		telnet-0.17-sock.patch
Patch10:	telnet-0.17-cleanup_race.patch
Patch11:	telnetd-0.17-pty_read.patch
Patch12:	telnet-0.17-CAN-2005-468_469.patch
Patch13:	telnet-0.17-cleanup_cleanup.patch
Patch14:	telnet-0.17-CAN-2005-0488.patch
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Telnet is a popular protocol for logging into remote systems over
the Internet. The telnet package provides a command line telnet
client.

%package	server
Summary:	A extremely unsecure telnet server
Group:		System/Servers

%description	server
Telnet is a popular protocol for logging into remote systems over
the Internet. Install the telnetd package if you want to support
extremely unsecure remote logins to your machine.

NOTE: because telnetd is unsecure you have to manually activate
it, this package will not do that for you. Instead use OpenSSH if
you want a secure server.

%prep 

%setup -q -n netkit-telnet-%{version}
mv telnet telnet-NETKIT
%setup -T -D -q -a 2 -n netkit-telnet-%{version}

%patch0 -p0 -b .cvs
%patch1 -p0 -b .fix
%patch2 -p1 -b .env
%patch3 -p0 -b .pek
%patch4 -p1 -b .issue
%patch5 -p1 -b .sa-01-49
%patch6 -p1 -b .8bit
%patch7 -p1 -b .argv
%patch8 -p1 -b .confverb
%patch9 -p1 -b .socket

%patch10 -p1 -b .cleanup_race 
%patch11 -p0 -b .pty_read
%patch12 -p1 -b .CAN-2005-468_469
%patch13 -p1 -b .cleanup_cleanup
%patch14 -p1 -b .CAN-2005-0488

# only build the telnet client
#perl -pi -e "s|^SUB.*|SUB = telnet|g" Makefile

%build
sh configure --with-c-compiler=gcc
perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

# remove stripping
perl -pi -e 's|install[ ]+-s|install|g' \
	./telnet/GNUmakefile \
	./telnetd/Makefile \
	./telnetlogin/Makefile \
	./telnet-NETKIT/Makefile

make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man8

install -m0755 telnet/telnet  %{buildroot}%{_bindir}/netkit-telnet
install -m0644 telnet/telnet.1 %{buildroot}%{_mandir}/man1/netkit-telnet.1
install -m0755 telnetd/telnetd  %{buildroot}%{_sbindir}/netkit-telnetd
install -m0644 telnetd/telnetd.8 %{buildroot}%{_mandir}/man8/netkit-telnetd.8

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README
%attr(0755,root,root) %{_bindir}/netkit-telnet
%attr(0644,root,root) %{_mandir}/man1/netkit-telnet.1*

%files server
%defattr(-,root,root)
%doc ChangeLog README
%attr(0755,root,root) %{_sbindir}/netkit-telnetd
%attr(0644,root,root) %{_mandir}/man8/netkit-telnetd.8*

