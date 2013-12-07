Summary:	Client for the telnet remote login protocol
Name:		netkit-telnet
Version:	0.17
Release:	18
License:	BSD
Group:		Networking/Remote access
Url:		ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/
Source0:	ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-telnet-%{version}.tar.gz
Source2:	telnet-client.tar.gz
Patch1:		telnet-client-cvs.patch
Patch5:		telnetd-0.17.diff
Patch6:		telnet-0.17-env.patch
Patch7:		telnet-0.17-issue.patch
Patch8:		telnet-0.17-sa-01-49.patch
Patch9:		telnet-0.17-env-5x.patch
Patch10:	telnet-0.17-pek.patch
Patch11:	telnet-0.17-8bit.patch
Patch12:	telnet-0.17-argv.patch
Patch13:	telnet-0.17-conf.patch
Patch14:	telnet-0.17-cleanup_race.patch
Patch15:	telnetd-0.17-pty_read.patch
Patch16:	telnet-0.17-CAN-2005-468_469.patch
Patch17:	telnet-0.17-linemode.patch
Patch18:	telnet-gethostbyname.patch
Patch19:	netkit-telnet-0.17-ipv6.diff
Patch20:	netkit-telnet-0.17-nodns.patch
Patch21:	telnet-0.17-errno_test_sys_bsd.patch
Patch22:	netkit-telnet-0.17-reallynodns.patch
#
Patch100:	telnet-0.17-sock.patch
Patch101:	telnet-0.17-cleanup_cleanup.patch
Patch102:	telnet-0.17-CAN-2005-0488.patch
Patch103:	netkit-telnet-0.17-format_not_a_string_literal_and_no_format_arguments.diff
Patch104:	netkit-telnet-0.17-CVE-2011-4862.diff
BuildRequires:	gpm-devel
BuildRequires:	pkgconfig(ncurses)
Provides:	telnet-client
Conflicts:	krb5-appl-clients
Conflicts: 	heimdal-telnet

%description
Telnet is a popular protocol for logging into remote systems over
the Internet. The telnet package provides a command line telnet
client.

%package	server
Summary:	A extremely unsecure telnet server
Group:		System/Servers
Provides:	telnetd = %{version}-%{release}
Obsoletes:	telnetd < %{version}-%{release}
Provides:	telnet-server
Conflicts:	krb5-appl-servers
Conflicts:	heimdal-telnetd

%description	server
Telnet is a popular protocol for logging into remote systems over
the Internet. Install the telnetd package if you want to support
extremely unsecure remote logins to your machine.

NOTE: because telnetd is unsecure you have to manually activate
it, this package will not do that for you. Instead use OpenSSH if
you want a secure server.

%prep 

%setup -q
mv telnet telnet-NETKIT
%setup -T -D -q -a 2 -n netkit-telnet-%{version}
%patch1 -p0 -b .cvs
%patch5 -p0 -b .fix
%patch6 -p1 -b .env
%patch10 -p0 -b .pek
%patch7 -p1 -b .issue
%patch8 -p1 -b .sa-01-49
%patch11 -p1 -b .8bit
%patch12 -p1 -b .argv
%patch13 -p1 -b .confverb
%patch14 -p1 -b .cleanup_race 
%patch15 -p0 -b .pty_read
%patch16 -p1 -b .CAN-2005-468_469
#%patch17 -p1 -b .linemode
%patch18 -p1 -b .gethost
%patch19 -p1 -b .gethost2
%patch20 -p1 -b .nodns
%patch21 -p1 -b .errnosysbsd
%patch22 -p1 -b .reallynodns
#
%patch100 -p1 -b .socket
%patch101 -p1 -b .cleanup_cleanup
%patch102 -p1 -b .CAN-2005-0488
%patch103 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch104 -p0 -b .CVE-2011-4862

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
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man8

install -m0755 telnet/telnet  %{buildroot}%{_bindir}/telnet
install -m0644 telnet/telnet.1 %{buildroot}%{_mandir}/man1/telnet.1
install -m0755 telnetd/telnetd  %{buildroot}%{_sbindir}/telnetd
install -m0644 telnetd/telnetd.8 %{buildroot}%{_mandir}/man8/telnetd.8

%files
%doc ChangeLog README
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*

%files server
%{_sbindir}/telnetd
%{_mandir}/man8/telnetd.8*

