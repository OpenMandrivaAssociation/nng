%global debug_package %{nil}

Name:		nng
Version:	1.10.1
Release:	2
Source0:	https://github.com/nanomsg/nng/archive/refs/tags/v%{version}/nng-%{version}.tar.gz
Summary:	Nanomsg-Next-Generation light-weight brokerless messaging
URL:		https://github.com/nng/nng
License:	MIT
Group:		System/Libraries
BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  lib64mbedtls-devel
BuildRequires:  lib64nsl2
BuildRequires:  asciidoctor

%description
NNG provides a common messaging framework intended to solve common communication
problems in distributed applications. It offers a number of protocols, and also
a number of transports.

The protocols implement the semantics associated with particular communications
scenarios, such as RPC style services, service discovery,
publish/subscribe, and so forth.

The transports provide support for underlying transport methods,
such as TCP, IPC, websockets, and so forth.

NNG is designed to permit easy creation of new transports and to a lesser
extent, new protocols.

NNG is wire compatible with the SP protocols described in the nanomsg project;
projects using libnanomsg can inter-operate with nng as well as other conforming
implementations. (One such implementation is mangos.)

Applications using NNG which wish to communicate with other libraries must
ensure that they only use protocols or transports offered by the other library.

NNG also offers a compatible API, permitting legacy code to be recompiled or
re-linked against NNG. When doing this, support for certain enhancements or
features will likely be absent, requiring the application developer to use
the new-style API.

NNG is implemented in pure C; if you need bindings for other languages
please check the website.

############################
%package    devel
Summary:    Development files for the nng socket library
Group:      Development/C
Requires:   %{name} = %{version}-%{release}

%description    devel
This package contains the header files needed to develop applications using nng,
a socket library that provides several communication patterns

############################
%package    utils
Summary:    Command line interface for communication with nng
Requires:   %{name} = %{version}-%{release}

%description    utils
Includes the nngcat utility which provides command line access to the
Scalability Protocols, making it possible to write shell scripts that interact
with other peers in a Scalability Protocols topology, by both sending and
receiving messages.

############################
%prep
%autosetup -p1

############################
%build
cmake   -G Ninja -DCMAKE_INSTALL_PREFIX="/usr" \
        -DCMAKE_CXX_FLAGS="%optflags -fPIC" \
        -DBUILD_SHARED_LIBS=ON \
        -DNNG_ENABLE_TLS=ON \
        -DNNG_ENABLE_NNGCAT=ON \
        -DNNG_TESTS=ON \
        -DNNG_ENABLE_DOC=ON
ninja -C .

############################
%install
DESTDIR="%{buildroot}" ninja -C %{_builddir}/%{name}-%{version} install

# workaround for rpmlint non-versioned-file-in-library-package tomfoolery
mkdir -p %{buildroot}%{_defaultlicensedir}/%{name}-%{version}/
cp -p LICENSE.txt %{buildroot}%{_defaultlicensedir}/%{name}-%{version}/LICENSE.txt

# housekeeping: copy doc/*.html into doc/html/ path
mkdir -p %{buildroot}%{_docdir}/%{name}/html/
cp -p %{buildroot}%{_docdir}/%{name}/*.html %{buildroot}%{_docdir}/%{name}/html
rm %{buildroot}%{_docdir}/%{name}/*.html

############################
%files
%{_libdir}/libnng.so.1*
%{_defaultlicensedir}/%{name}-%{version}/LICENSE.txt

%files  devel
%{_includedir}/%{name}/
%{_libdir}/libnng.so
%{_libdir}/cmake/%{name}/
%{_mandir}/man*/*.3*
%{_mandir}/man*/*.5*
%{_mandir}/man*/*.7*
%{_docdir}/%{name}/html/*.html

%files  utils
%{_bindir}/nngcat
%{_mandir}/man*/*.1*
