#
# Conditional build:
%bcond_without	static_libs	# static library build
#
Summary:	Library for searching Approximate Nearest Neighbors
Summary(pl.UTF-8):	Biblioteka do przybliżonego wyszukiwania najbliższych sąsiadów
Name:		ann
Version:	1.1.2
Release:	2
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: http://www.cs.umd.edu/~mount/ANN/
Source0:	http://www.cs.umd.edu/~mount/ANN/Files/%{version}/%{name}_%{version}.tar.gz
# Source0-md5:	7ffaacc7ea79ca39d4958a6378071365
Patch0:		%{name}-make.patch
Patch1:		%{name}-gcc43.patch
URL:		http://www.cs.umd.edu/~mount/ANN/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ANN is a library written in the C++ programming language to support
both exact and approximate nearest neighbor searching in spaces of
various dimensions.

%description -l pl.UTF-8
ANN to napisana w języku C++ biblioteka do zarówno dokładnego, jak i
przybliżonego wyszukiwania najbliższych sąsiadów w przestrzeniach o
różnej liczbie wymiarów.

%package devel
Summary:	Header files for ANN library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ANN
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for ANN library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ANN.

%package static
Summary:	Static ANN library
Summary(pl.UTF-8):	Statyczna biblioteka ANN
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ANN library.

%description static -l pl.UTF-8
Statyczna biblioteka ANN.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with static_libs}
# static
%{__make} -C src targets \
	ANNLIB="libANN.a" \
	"C++ = %{__cxx}" \
	CFLAGS="%{rpmcxxflags}" \
	MAKELIB="ar ruv" \
	RANLIB=true
%{__rm} src/*.o
%endif

# shared
for d in src ann2fig ; do
%{__make} -C $d targets \
	ANNLIB="libANN.so.1.0" \
	ANNDEVLIB="libANN.so" \
	"C++ = %{__cxx}" \
	CFLAGS="%{rpmcxxflags} -fPIC" \
	MAKELIB="%{__cxx} %{rpmldflags} -shared -Wl,-soname,libANN.so.1 -o" \
	RANLIB=true
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/ANN,%{_pkgconfigdir}}

install bin/ann2fig $RPM_BUILD_ROOT%{_bindir}
%{?with_static_libs:install lib/libANN.a $RPM_BUILD_ROOT%{_libdir}}
install lib/libANN.so.1.0 $RPM_BUILD_ROOT%{_libdir}
ln -sf libANN.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libANN.so.1
ln -sf libANN.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libANN.so
cp -p include/ANN/*.h $RPM_BUILD_ROOT%{_includedir}/ANN

# create pkg-config file
cat >$RPM_BUILD_ROOT%{_pkgconfigdir}/ann.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: ann
Description: Library for searching Approximate Nearest Neighbors
Version: %{version}
Requires:
Libs: -L${libdir} -lANN
Cflags: -I${includedir}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Copyright.txt ReadMe.txt
%attr(755,root,root) %{_bindir}/ann2fig
%attr(755,root,root) %{_libdir}/libANN.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libANN.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/ANNmanual.pdf
%attr(755,root,root) %{_libdir}/libANN.so
%{_includedir}/ANN
%{_pkgconfigdir}/ann.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libANN.a
%endif
