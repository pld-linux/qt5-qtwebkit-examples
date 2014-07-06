#
# Conditional build:
%bcond_without	qch		# documentation in QCH format

%define		orgname			qtwebkit-examples
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qtscript_ver		%{version}
%define		qttools_ver		%{version}
%define		qtwebkit_ver		%{version}
%define		qtxmlpatterns_ver	%{version}
Summary:	Qt5 WebKit examples
Summary(pl.UTF-8):	Przykłady do bibliotek Qt5 WebKit
Name:		qt5-%{orgname}
Version:	5.3.1
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.3/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	5827c61adba1d6921c51ef7ba1adce68
URL:		http://qt-project.org/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt5Concurrent-devel >= %{qtbase_ver}
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
BuildRequires:	Qt5OpenGL-devel >= %{qtbase_ver}
BuildRequires:	Qt5PrintSupport-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Sql-devel >= %{qtbase_ver}
BuildRequires:	Qt5WebKit-devel >= %{qtwebkit_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
BuildRequires:	Qt5XmlPatterns-devel >= %{qtxmlpatterns_ver}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.654
%if %{with qch}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 WebKit examples.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera przykłady do bibliotek Qt5 WebKit.

%package doc
Summary:	Qt5 WebKit examples documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja przykładów do bibliotek Qt5 WebKit w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 WebKit examples documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja przykładów do bibliotek Qt5 WebKit w formacie HTML.

%package doc-qch
Summary:	Qt5 WebKit examples documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja przykładów do bibliotek Qt5 WebKit w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 WebKit examples documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja przykładów do bibliotek Qt5 WebKit w formacie QCH.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5

%{__make}
%{__make} %{!?with_qch:html_}docs

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/webkitqml
ifecho_tree examples %{_examplesdir}/qt5/webkitwidgets

%clean
rm -rf $RPM_BUILD_ROOT

%files -f examples.files
%defattr(644,root,root,755)
%doc dist/changes-*
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebkitexamples

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebkitexamples.qch
%endif
