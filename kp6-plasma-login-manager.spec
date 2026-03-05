#
# TODO: pld pam config file
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.6.2
%define		qtver		6.10.0
%define		kpname		plasma-login-manager

Summary:	Plasma Login Manager
Name:		kp6-%{kpname}
Version:	6.6.2
Release:	2
License:	GPL v2+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	a09021d5c936b4ff46ebbfa3b18c92de
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 6.10.0
BuildRequires:	Qt6Qml-devel >= 6.8.0
BuildRequires:	Qt6Quick-devel >= 6.8.0
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= 6.22.0
BuildRequires:	kf6-kauth-devel >= 6.22.0
BuildRequires:	kf6-kcmutils-devel >= 6.22.0
BuildRequires:	kf6-kconfig-devel >= 6.23.0
BuildRequires:	kf6-kdbusaddons-devel >= 6.22.0
BuildRequires:	kf6-ki18n-devel >= 6.22.0
BuildRequires:	kf6-kio-devel >= 6.22.0
BuildRequires:	kf6-kirigami-devel >= 6.22.0
BuildRequires:	kp6-layer-shell-qt-devel >= %{kdeplasmaver}
BuildRequires:	kp6-libkscreen-devel >= %{kdeplasmaver}
BuildRequires:	kp6-libplasma-devel >= %{kdeplasmaver}
BuildRequires:	kp6-plasma-workspace-devel >= %{kdeplasmaver}
BuildRequires:	ninja
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Plasma Login provides a display manager for KDE Plasma, forked from
[SDDM](https://github.com/sddm/sddm) and with an new frontend
providing a greeter, wallpaper plugin integration and System Settings
module (KCM).

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DINSTALL_PAM_CONFIGURATION:BOOL=OFF \
	-DKDE_INSTALL_SYSTEMDUNITDIR=/lib/systemd \
	-DKDE_INSTALL_SYSTEMDUSERUNITDIR=/usr/lib/systemd/user

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/plasma-login-wallpaper
%attr(755,root,root) %{_bindir}/plasmalogin
%attr(755,root,root) %{_bindir}/startplasma-login-wayland
%{systemdunitdir}/plasmalogin.service
%{systemduserunitdir}/plasma-login-kwin_wayland.service
%{systemduserunitdir}/plasma-login-wayland.target
%{systemduserunitdir}/plasma-login.service
%{systemduserunitdir}/plasma-wallpaper.service
%{_prefix}/lib/sysusers.d/plasmalogin.conf
%{systemdtmpfilesdir}/plasmalogin.conf
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_plasmalogin.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/kcmplasmalogin_authhelper
%attr(755,root,root) %{_prefix}/libexec/plasma-login-greeter
%attr(755,root,root) %{_prefix}/libexec/plasmalogin-helper
%attr(755,root,root) %{_prefix}/libexec/plasmalogin-helper-start-x11user
%{_desktopdir}/kcm_plasmalogin.desktop
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmplasmalogin.service
%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_datadir}/dbus-1/system.d/org.kde.kcontrol.kcmplasmalogin.conf
%dir %{_datadir}/plasmalogin
%dir %{_datadir}/plasmalogin/scripts
%attr(755,root,root) %{_datadir}/plasmalogin/scripts/Xsession
%attr(755,root,root) %{_datadir}/plasmalogin/scripts/Xsetup
%attr(755,root,root) %{_datadir}/plasmalogin/scripts/Xstop
%attr(755,root,root) %{_datadir}/plasmalogin/scripts/wayland-session
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmplasmalogin.policy
