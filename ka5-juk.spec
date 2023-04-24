#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.04.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		juk
Summary:	Juk
Name:		ka5-%{kaname}
Version:	23.04.0
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Multimedia
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	87f1aead665d02c8ff91c83912f466eb
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-kwallet-devel >= %{kframever}
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

%description -l pl.UTF-8
JuK to aplikacja szafy grającej, obsługująca kolekcje plików MP3,
Ogg Vorbis i FLAC. Program pozwala edytować tagi plików dźwiękowych,
zarządzać kolekcjami i listami odtwarzania. Głównie kładzie nacisk
na zarządzanie muzyką.

Właściwości

• Listy kolekcji i wiele definiowanych przez użytkownika playlist.
• Możliwość przeszukawania katalogów i automatyczne importowanie
  list odtwarzania i plików muzycznych na starcie.
• Dynamiczne przeszukiwanie playlist, które są automatycznie
  uaktualniane, gdy jakieś pola w kolekcji się zmienią.
• Tryb widoku drzewa, gdzie playlisty są automatycznie generowane
  dla zestawów albumów, artystów i gatunków muzycznych.
• Historia odtwarzania, która wskazuje które pliki były odtwarzane
  i kiedy.
• Przeszukiwanie i filtrowanie widocznych elementów listy.
• Możliwość odgadnięcia informacji o tagach na podstawie nazwy pliku
  lub korzystając z zapytań do bazy MusicBrainz online.
• Inteligentne zmiany nazw plików na podstawie tagów.
• Czytanie i edycja znaczników ID3v1, ID3v2 i Ogg Vorbis (przy użyciu
  TagLib).

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie
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
%{_datadir}/kxmlgui5/juk
%{_datadir}/knotifications5/juk.notifyrc
/usr/share/kio/servicemenus/jukservicemenu.desktop
