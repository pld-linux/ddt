Summary:	Dynamic DNS Tools Server
Summary(pl):	Serwer dynamicznego DNSu
Name:		ddt
Version:	0.5.9
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	30bb784bde3eef1e1a6eb61ab77f4b90
Patch0:		%{name}-am_ac.patch
Patch1:		%{name}-cgi-to-cgic.patch
Patch2:		%{name}-bind-includes-hack.patch
Patch3:		%{name}-nobody.patch
Patch4:		%{name}-postgresql.patch
URL:		http://www.ddts.org/
Source1:	%{name}-client.init
Source2:	%{name}-server.init
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bind-devel >= 9.2.1-10
BuildRequires:	cgilibc-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	macrosystem-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	opt
BuildRequires:	postgresql-c++-devel
BuildRequires:	regexx-devel
BuildRequires:	sgml-tools
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DDT stands for Dynamic Dns Tools. The goal of the project is to
provide an open and free (in the GPL-sense) set of tools that will
permit the deployment of secure and reliable dynamic DNS services.

%description -l pl
DDT oznacza Dynamiczne Narzêdzia DNS. Celem projektu jest dostarczenie
otwartego i wolnego (w sensie GPL) zestawu narzêdzi pozwalaj±cych na
stworzenie bezpiecznego i niezawodnego systemu dynamicznego DNS.

%package clients
Summary:	Dynamic DNS Tools Client
Summary(pl):	Klient Dynamicznego DNSu
Group:		Applications/Networking
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig

%description clients
Dynamic DNS Tools Client.

%description clients -l pl
Klient Dynamicznego DNSu.

%package cgi
Summary:        CGI scripts for Dynamic DNS Tools Server
Summary(pl):    Skrypty CGI do Serwera Dynamicznego DNSu
Group:          Applications/Networking
Requires:	webserver

%description cgi
CGI scripts for Dynamic DNS Tools Server.

%description cgi -l pl
Skrypty CGI do Serwera Dynamicznego DNSu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
CPPFLAGS="-I%{_includedir}/cgilibc -I%{_includedir}/postgresql/server"; export CPPFLAGS
%configure \
	--enable-docs \
	--enable-server \
	--enable-admin \
	--with-pgsql-incdir=%{_includedir} \
	--with-pgsql-libdir=%{_libdir}
# fixme
echo "all install:" > docs/Makefile

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT{/etc/logrotate.d,/var/{lib/ddt-client,run/ddt}} \
	$RPM_BUILD_ROOT/home/services/httpd/{cgi-bin,html/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
	
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-client
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-server
install debian/ddt-client.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/%{name}-client
install debian/ddt-server.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/%{name}-server

install admin/templates/* $RPM_BUILD_ROOT/home/services/httpd/html/%{name}
install admin/*.{conf,cgi} $RPM_BUILD_ROOT/home/services/httpd/cgi-bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}-server
if [ -f /var/lock/subsys/%{name}-server ]; then
	/etc/rc.d/init.d/%{name}-server restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name}-server start\" to start ddtd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name}-server ]; then
		/etc/rc.d/init.d/%{name}-server stop >&2
	fi
	/sbin/chkconfig --del %{name}-server
fi

%post clients
/sbin/chkconfig --add %{name}-client
if [ -f /var/lock/subsys/%{name}-client ]; then
        /etc/rc.d/init.d/%{name}-client restart >&2
else
        echo "Run \"/etc/rc.d/init.d/%{name}-client start\" to start ddtcd daemon."
fi

%preun clients
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name}-client ]; then
                /etc/rc.d/init.d/%{name}-client stop >&2
        fi
        /sbin/chkconfig --del %{name}-client
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS NEWS README THANKS TODO
%doc docs/*.sgml docs/include/{named.conf,zonedb}
%doc server/*.sql
%attr(754,root,root) /etc/rc.d/init.d/%{name}-server
%attr(755,root,root) %{_sbindir}/ddtd
%{_mandir}/man8/ddtd.8*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/ddtd.conf
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/%{name}-server
%attr(644,root,root) %dir /var/lib/ddt-client
%attr(644,root,root) %dir /var/run/ddt

%files clients
%defattr(644,root,root,755)
%doc docs/DDT*.sgml
%attr(754,root,root) /etc/rc.d/init.d/%{name}-client
%attr(755,root,root) %{_sbindir}/ddtc
%attr(755,root,root) %{_sbindir}/ddtcd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/ddtcd.conf
%{_mandir}/man8/ddtc.8*
%{_mandir}/man8/ddtcd.8*
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/%{name}-client

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) /home/services/httpd/cgi-bin/*.cgi
%attr(644,root,root) /home/services/httpd/cgi-bin/*.conf
%attr(755,root,root) /home/services/httpd/html/%{name}
