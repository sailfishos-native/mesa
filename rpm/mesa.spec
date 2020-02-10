
%ifarch %{ix86} x86_64
%global with_intel     1
%endif

%ifarch %{arm} aarch64
%global with_freedreno 1
%global with_kmsro     1
%global with_lima      1
%global with_panfrost  1
%global with_tegra     1
%global with_vc4       1
%endif


Name:       mesa

Summary:    Mesa graphics libraries
Version:    19.3.3
Release:    0
Group:      System/Libraries
License:    MIT
URL:        http://www.mesa3d.org/
Source0:    %{name}-%{version}.tar.bz2
Patch1:     disable-avx-support.diff

BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(talloc)
BuildRequires:  pkgconfig(libudev) >= 160
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig meson
BuildRequires:  expat-devel >= 2.0
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  libxml2-python
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gettext

%description
Mesa is an open-source implementation of the OpenGL specification  -
a system for rendering interactive 3D graphics.

%package libgbm
Summary:    Generic buffer management API
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   libgbm = %{version}-%{release}

%description libgbm
Generic buffer management API

%package libgbm-devel
Summary:    Mesa libgbm development package
Group:      System/Libraries
Requires:   %{name}-libgbm = %{version}-%{release}
Provides:   libgbm-devel

%description libgbm-devel
Mesa libgbm development package.

%package libglapi
Summary:    Mesa shared gl api library
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libglapi
Mesa shared gl api library.

%package libGLESv1
Summary:    Mesa libGLESv1 runtime libraries
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   libGLESv1 = %{version}-%{release}

%description libGLESv1
Mesa libGLESv1 runtime library.

%package libGLESv2
Summary:    Mesa libGLESv2 runtime libraries
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   libGLESv2 = %{version}-%{release}

%description libGLESv2
Mesa libGLESv2 runtime library.

%package libEGL
Summary:    Mesa libEGL runtime libraries and DRI drivers
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   libEGL = %{version}-%{release}

%description libEGL
Mesa libEGL runtime library.

%package libglapi-devel
Summary:    Mesa libglapi development package
Group:      System/Libraries
Requires:   %{name}-libglapi = %{version}-%{release}
Provides:   libglapi-devel

%description libglapi-devel
Mesa libglapi development package.

%package libGLESv1-devel
Summary:    Mesa libGLESv1 development package
Group:      Development/Libraries
Requires:   %{name}-libGLESv1 = %{version}-%{release}
Provides:   libGLESv1-devel

%description libGLESv1-devel
Mesa libGLESv1 development packages

%package libGLESv2-devel
Summary:    Mesa libGLESv2 development package
Group:      Development/Libraries
Requires:   %{name}-libGLESv2 = %{version}-%{release}
Provides:   libGLESv2-devel

%description libGLESv2-devel
Mesa libGLESv2 development packages

%package libEGL-devel
Summary:    Mesa libEGL development package
Group:      Development/Libraries
Requires:   %{name}-libEGL = %{version}-%{release}
Provides:   libEGL-devel

%description libEGL-devel
Mesa libEGL development packages

%package libGL-devel
Summary:    Mesa libGL development package
Group:      Development/Libraries
Requires:   %{name}-libGL = %{version}-%{release}
Provides:   libGL-devel

%description libGL-devel
Mesa libGL development packages

%package dri-drivers
Summary:    Mesa-based DRI drivers
Group:      Graphics/Display and Graphics Adaptation
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   mesa-dri-drivers = %{version}-%{release}

%description dri-drivers
Mesa-based dri drivers.

%package dri-drivers-devel
Summary:    Mesa-based DRI development files
Group:      Development/Libraries

%description dri-drivers-devel
Mesa-based DRI driver development files.

%prep
%setup -q -n %{name}-%{version}/mesa

%build
%meson   -Ddri-drivers=%{?with_intel:,i915,i965} \
    -Dosmesa=none \
    -Ddri3=false \
    -Dllvm=false \
    -Dshared-llvm=false \
    -Dgallium-drivers=swrast,nouveau,%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_kmsro:,kmsro}%{?with_lima:,lima}%{?with_panfrost:,panfrost} \
    -Dvulkan-drivers= \
    -Dplatforms=drm,wayland \
    -Dglx=disabled \
    -Degl=true \
    -Dgles1=true \
    -Dgles2=true \
    -Dgallium-xa=false \
    -Dprefer-iris=false

%meson_build

%install
%meson_install

# Remove empty file created by build
rm -rf %{buildroot}/%{_libdir}/dri/kms_swrast_dri.so

%post libgbm -p /sbin/ldconfig

%postun libgbm -p /sbin/ldconfig

%post libglapi -p /sbin/ldconfig

%postun libglapi -p /sbin/ldconfig

%post libGLESv1 -p /sbin/ldconfig

%postun libGLESv1 -p /sbin/ldconfig

%post libGLESv2 -p /sbin/ldconfig

%postun libGLESv2 -p /sbin/ldconfig

%post libEGL -p /sbin/ldconfig

%postun libEGL -p /sbin/ldconfig

%post dri-drivers -p /sbin/ldconfig

%postun dri-drivers -p /sbin/ldconfig


%files libgbm
%defattr(-,root,root,-)
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*

%files libgbm-devel
%defattr(-,root,root,-)
/usr/include/gbm.h
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/gbm.pc

%files libglapi
%defattr(-,root,root,-)
%{_libdir}/libglapi.so.0
%{_libdir}/libglapi.so.0.*

%files libGLESv1
%defattr(-,root,root,-)
%{_libdir}/libGLESv1_CM.so.*

%files libGLESv2
%defattr(-,root,root,-)
%{_libdir}/libGLESv2.so.*

%files libEGL
%defattr(-,root,root,-)
%{_libdir}/libEGL.so.*

%files libglapi-devel
%defattr(-,root,root,-)
%{_libdir}/libglapi.so

%files libGLESv1-devel
%defattr(-,root,root,-)
%{_libdir}/libGLESv1_CM.so
%{_includedir}/GLES/egl.h
%{_includedir}/GLES/gl.h
%{_includedir}/GLES/glext.h
%{_includedir}/GLES/glplatform.h
%{_libdir}/pkgconfig/glesv1_cm.pc

%files libGLESv2-devel
%defattr(-,root,root,-)
%{_libdir}/libGLESv2.so
%{_includedir}/GLES2/gl2.h
%{_includedir}/GLES2/gl2ext.h
%{_includedir}/GLES2/gl2platform.h
%{_includedir}/GLES3/gl3.h
%{_includedir}/GLES3/gl31.h
%{_includedir}/GLES3/gl32.h
%{_includedir}/GLES3/gl3ext.h
%{_includedir}/GLES3/gl3platform.h
%{_libdir}/pkgconfig/glesv2.pc

%files libEGL-devel
%defattr(-,root,root,-)
%{_libdir}/libEGL.so
%dir %{_includedir}/EGL
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/eglextchromium.h
%{_includedir}/EGL/eglplatform.h
%{_includedir}/EGL/eglmesaext.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc

%files libGL-devel
%defattr(-,root,root,-)
%{_includedir}/GL/gl.h
%{_includedir}/GL/glcorearb.h
%{_includedir}/GL/glext.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files dri-drivers-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/dri.pc

%files dri-drivers
%defattr(-,root,root,-)
%dir %{_datadir}/drirc.d
%{_datadir}/drirc.d/00-mesa-defaults.conf
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/nouveau_dri.so
%ifarch %{arm} aarch64
%{_libdir}/dri/imx-drm_dri.so
%endif
%if 0%{?with_lima}
%{_libdir}/dri/lima_dri.so
%endif
%if 0%{?with_intel}
%{_libdir}/dri/i915_dri.so
%{_libdir}/dri/i965_dri.so
%endif
%if 0%{?with_vc4}
%{_libdir}/dri/vc4_dri.so
%endif
%if 0%{?with_freedreno}
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%endif
%if 0%{?with_etnaviv}
%{_libdir}/dri/etnaviv_dri.so
%endif
%if 0%{?with_tegra}
%{_libdir}/dri/tegra_dri.so
%endif
%if 0%{?with_panfrost}
%{_libdir}/dri/panfrost_dri.so
%endif
%if 0%{?with_kmsro}
%{_libdir}/dri/armada-drm_dri.so
%{_libdir}/dri/exynos_dri.so
%{_libdir}/dri/hx8357d_dri.so
%{_libdir}/dri/ili9225_dri.so
%{_libdir}/dri/ili9341_dri.so
%{_libdir}/dri/meson_dri.so
%{_libdir}/dri/mi0283qt_dri.so
%{_libdir}/dri/pl111_dri.so
%{_libdir}/dri/repaper_dri.so
%{_libdir}/dri/rockchip_dri.so
%{_libdir}/dri/st7586_dri.so
%{_libdir}/dri/st7735r_dri.so
%{_libdir}/dri/sun4i-drm_dri.so
%{_libdir}/dri/mxsfb-drm_dri.so
%{_libdir}/dri/stm_dri.so
%{_libdir}/dri/ingenic-drm_dri.so
%{_libdir}/dri/mcde_dri.so
%endif
