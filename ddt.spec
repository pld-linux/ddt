Summary:	Dynamic DNS Tools Server
Summary(pl):	Serwer dynamicznego DNSu
Name:		ddt
Version:	0.5
Release:	1
Group:		Networking/Daemons
License:	GPL
URL:		http://www.ddt.org/
Source0:	http://download.sourceforge.net/ddt/ddt-0.5.tar.gz
Patch0:		%{name}-am_ac.patch
Source1:	%{name}.init
BuildRequires:	opt
BuildRequires:	openssl-devel
BuildRequires:	bind-devel >= 9.2.1-10
BuildRequires:	cgilib-devel
BuildRequires:	autoconf
BuildRequires:	automake
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DDT stands for Dynamic Dns Tools. The goal of the project is to
provide an open and free (in the GPL-sense) set of tools that will
permit the deployment of secure and reliable dynamic DNS services.

%description -l pl
DDT oznacza Dynamiczne Narzêdzia DNS. Celem projektu jest dostarczenie
otwartego i wolnego (w sensie GPL) zestawu narzêdzi pozwalaj±cych
na stworzenie bezpiecznego i niezawodnego systemu dynamicznego DNS.

%package clients
Summary:        Dynamic DNS Tools Client
Summary(pl):	Klient Dynamicznego DNSu
Group:          Applications/Networking

%description clients
Dynamic DNS Tools Client.

%description -l pl clients
Klient Dynamicznego DNSu.

%prep
%setup -q
%patch0 -p1

%build
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
install -d ${RPM_BUILD_ROOT}%{_sbindir}
install -d ${RPM_BUILD_ROOT}%{_mandir}/man8
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}
install -d ${RPM_BUILD_ROOT}/etc/rc.d/init.d
install -m640 client/ddtcd.conf $RPM_BUILD_ROOT/%{_sysconfdir}
install -m755 $RPM_SOURCE_DIR/ddtcd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/ddtcd
install -m755 client/ddtc $RPM_BUILD_ROOT/%{_sbindir}
install -m755 client/ddtcd $RPM_BUILD_ROOT/%{_sbindir}
gzip client/ddtc.8
gzip client/ddtcd.8
install -m755 client/ddtc*[.]8.gz $RPM_BUILD_ROOT/%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ddtcd

%preun
if [ $1 = 0 ]; then
   /sbin/chkconfig --del ddtcd
fi

%files
%defattr(644,root,root,755)
%config %{_sysconfdir}/ddtcd.conf
%doc AUTHORS README INSTALL COPYING THANKS ddt.lsm
%{_mandir}/man8/ddtc.8*
%{_mandir}/man8/ddtcd.8*
%attr(755,root,root) %{_sbindir}/ddtc
%attr(755,root,root) %{_sbindir}/ddtcd
/etc/rc.d/init.d/ddtcd
