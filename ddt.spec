Summary:	Dynamic DNS Tools Server
Summary(pl):	Serwer dynamicznego DNSu
Name:		ddt
Version:	0.5
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://download.sourceforge.net/ddt/%{name}-%{version}.tar.gz
Patch0:		%{name}-am_ac.patch
URL:		http://www.ddt.org/
Source1:	%{name}.init
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bind-devel >= 9.2.1-10
BuildRequires:	cgilib-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	opt
Prereq:		chkconfig
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

%description clients
Dynamic DNS Tools Client.

%description clients -l pl
Klient Dynamicznego DNSu.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-docs \
	--enable-server \
	--enable-admin \
	--with-pgsql-lib=%{_libdir} \
	--with-pgsql-include=%{_includedir}/postgresql/server
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/rc.d/init.d}

install client/ddtcd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ddtcd

install client/{ddtc,ddtcd} $RPM_BUILD_ROOT%{_sbindir}
install client/{ddtc,ddtcd}.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ddtcd
if [ -f /var/lock/subsys/ddtcd ]; then
	/etc/rc.d/init.d/ddtcd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ddtcd start\" to start ddtcd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ddtcd ]; then
		/etc/rc.d/init.d/ddtcd stop >&2
	fi
	/sbin/chkconfig --del ddtcd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README INSTALL THANKS ddt.lsm
%attr(754,root,root) /etc/rc.d/init.d/ddtcd
%config(noreplace) %{_sysconfdir}/ddtcd.conf
%attr(755,root,root) %{_sbindir}/ddtc
%attr(755,root,root) %{_sbindir}/ddtcd
%{_mandir}/man8/ddtc.8*
%{_mandir}/man8/ddtcd.8*
