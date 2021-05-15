%define		kdeappsver	21.04.1
%define		kframever	5.56.0
%define		qtver		5.9.0
%define		kaname		juk
Summary:	Juk
Name:		ka5-%{kaname}
Version:	21.04.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Multimedia
Source0:	http://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	3189e43b7594fec23d1153d018de56c0
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-phonon-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JuK is an audio jukebox application, supporting collections of MP3,
Ogg Vorbis, and FLAC audio files. It allows you to edit the "tags" of
your audio files, and manage your collection and playlists. It's main
focus, in fact, is on music management.

Features

• Collection list and multiple user defined playlists
• Ability to scan directories to automatically import playlists and
  music files on start up
• Dynamic Search Playlists that are automatically updated as fields in
  the collection change.
• A Tree View mode where playlists are automatically generated for
  sets of albums, artists and genres.
• Playlist history to indicate which files have been played and when.
• Inline search for filtering the list of visible items.
• The ability to guess tag information from the file name or using
  MusicBrainz online lookup.
• File renamer that can rename files based on the tag content.
• ID3v1, ID3v2 and Ogg Vorbis tag reading and editing support (via
  TagLib).

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/juk
%{_datadir}/dbus-1/interfaces/org.kde.juk.collection.xml
%{_datadir}/dbus-1/interfaces/org.kde.juk.player.xml
%{_datadir}/dbus-1/interfaces/org.kde.juk.search.xml
%{_iconsdir}/hicolor/128x128/apps/juk.png
%{_iconsdir}/hicolor/16x16/apps/juk.png
%{_iconsdir}/hicolor/32x32/apps/juk.png
%{_iconsdir}/hicolor/48x48/apps/juk.png
%{_iconsdir}/hicolor/64x64/apps/juk.png
%{_datadir}/metainfo/org.kde.juk.appdata.xml
%{_desktopdir}/org.kde.juk.desktop
%{_datadir}/juk
%{_datadir}/kservices5/ServiceMenus/jukservicemenu.desktop
%{_datadir}/kxmlgui5/juk
%{_datadir}/knotifications5/juk.notifyrc
