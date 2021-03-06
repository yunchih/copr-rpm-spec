%define cross_arch      arm
%define cross_triplet   arm-linux-gnueabi
%define cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

%if 0%{!?cross_stage:1}
%define cross_stage     final
%endif

%if %{cross_stage} != "final"
%define pkg_suffix      -%{cross_stage}
%else
%define pkg_suffix      %{nil}
%endif

%if 0%{?fedora} >= 22
%define enable_ada      1
%else
%define enable_ada      0
%endif

%if %{cross_arch} == "arm"
  %define lib_dir_name        lib
%else
  %if %{cross_arch} == "arm64"
    %define lib_dir_name      lib64
  %else
    %define lib_dir_name      lib
  %endif
%endif

Name:       %{cross_triplet}-gcc%{pkg_suffix}
Version:    6.3.0
Release:    1%{?dist}
Summary:    The GNU Compiler Collection (%{cross_triplet})

Group:      Development/Languages
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL:        https://gcc.gnu.org
Source0:    https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2

BuildRequires: texinfo, gettext, flex, bison, zlib-devel, isl-devel
BuildRequires: gmp-devel, mpfr-devel, libmpc-devel, elfutils-libelf-devel
BuildRequires: %{cross_triplet}-filesystem
BuildRequires: %{cross_triplet}-binutils
Requires:   %{cross_triplet}-filesystem
Requires:   %{cross_triplet}-binutils
Provides:   %{cross_triplet}-gcc-stage1 = %{version}

%if %{cross_stage} == "pass2"
BuildRequires: %{cross_triplet}-glibc-stage1
Requires:   %{cross_triplet}-glibc-stage1
Provides:   %{cross_triplet}-gcc-stage2 = %{version}
%endif

%if %{cross_stage} == "final"
BuildRequires: %{cross_triplet}-glibc
BuildRequires: gcc-gnat, libstdc++-static
Requires:   %{cross_triplet}-glibc
Provides:   %{cross_triplet}-gcc-stage2 = %{version}
Provides:   %{cross_triplet}-gcc-stage3 = %{version}
%endif

%description


%prep
%setup -qTb 0 -n gcc-%{version}


%build
mkdir -p %{_builddir}/gcc-build
cd %{_builddir}/gcc-build
AR_FOR_TARGET=%{_bindir}/%{cross_triplet}-ar \
AS_FOR_TARGET=%{_bindir}/%{cross_triplet}-as \
DLLTOOL_FOR_TARGET=%{_bindir}/%{cross_triplet}-dlltool \
LD_FOR_TARGET=%{_bindir}/%{cross_triplet}-ld \
NM_FOR_TARGET=%{_bindir}/%{cross_triplet}-nm \
OBJDUMP_FOR_TARGET=%{_bindir}/%{cross_triplet}-objdump \
RANLIB_FOR_TARGET=%{_bindir}/%{cross_triplet}-ranlib \
STRIP_FOR_TARGET=%{_bindir}/%{cross_triplet}-strip \
WINDRES_FOR_TARGET=%{_bindir}/%{cross_triplet}-windres \
WINDMC_FOR_TARGET=%{_bindir}/%{cross_triplet}-windmc \
../gcc-%{version}/configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --host=%{_target_platform} \
    --build=%{_target_platform} \
    --target=%{cross_triplet} \
    --with-local-prefix=%{cross_sysroot} \
    --with-sysroot=%{cross_sysroot} \
    --with-linker-hash-style=gnu \
    --with-system-zlib \
    --with-isl \
    --disable-nls \
    --enable-lto \
    --enable-multilib \
    --enable-__cxa_atexit \
    --enable-initfini-array \
    --enable-linker-build-id \
    --enable-gnu-unique-object \
    --enable-gnu-indirect-function \
%if %{cross_arch} == "arm"
%if %(echo %{cross_triplet} | sed 's/.*-\([a-z]*\)$/\1/') == "gnueabihf"
    --with-tune=cortex-a8 \
    --with-arch=armv7-a \
    --with-float=hard \
    --with-fpu=vfpv3-d16 \
    --with-abi=aapcs-linux \
%endif
%endif
%if %{cross_stage} == "pass1"
    --with-newlib \
    --enable-languages=c \
    --disable-shared \
    --disable-threads \
    --disable-libmudflap \

make %{?_smp_mflags} all-gcc
%endif
%if %{cross_stage} == "pass2"
    --enable-languages=c \
    --enable-shared \
    --disable-libgomp \
    --disable-libmudflap \

make %{?_smp_mflags} all-gcc all-target-libgcc
%endif
%if %{cross_stage} == "final"
%if %{enable_ada}
    --enable-languages=c,c++,fortran,objc,obj-c++,ada \
%else
    --enable-languages=c,c++,fortran,objc,obj-c++ \
%endif
%if 0%{?fedora} <= 22
    --with-default-libstdcxx-abi=gcc4-compatible \
%endif
    --enable-libmulflap \
    --enable-libgomp \
    --enable-libssp \
    --enable-libquadmath \
    --enable-libquadmath-support \
    --enable-libsanitizer \
    --enable-gold \
    --enable-plugin \
    --enable-threads=posix \

make %{?_smp_mflags}
%endif


%install
cd %{_builddir}/gcc-build

%if %{cross_stage} == "pass1"
make install-gcc DESTDIR=%{buildroot}
%endif
%if %{cross_stage} == "pass2"
make install-gcc install-target-libgcc DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{cross_sysroot}/%{lib_dir_name}
mv %{buildroot}%{_prefix}/%{cross_triplet}/%{lib_dir_name}/* \
    %{buildroot}%{cross_sysroot}/%{lib_dir_name}
rmdir %{buildroot}%{_prefix}/%{cross_triplet}/%{lib_dir_name}
%endif
%if %{cross_stage} == "final"
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{cross_sysroot}/%{lib_dir_name}
mv %{buildroot}%{_prefix}/%{cross_triplet}/%{lib_dir_name}/* \
    %{buildroot}%{cross_sysroot}/%{lib_dir_name}
rmdir %{buildroot}%{_prefix}/%{cross_triplet}/%{lib_dir_name}
%endif

find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_datadir}/gcc-%{version}/python
rm -f %{buildroot}%{_bindir}/%{cross_triplet}-gcc-%{version}
rm -f %{buildroot}%{_libdir}/libcc1.so*
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/install-tools
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools/fixincl
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools/fixinc.sh
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools/mkheaders
rm -f %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools/mkinstalldirs
rmdir --ignore-fail-on-non-empty %{buildroot}%{_libexecdir}/gcc/%{cross_triplet}/%{version}/install-tools

# Don't strip libgcc.a and libgcov.a - based on Fedora Project cross-gcc.spec
%define __ar_no_strip $RPM_BUILD_DIR/gcc-%{version}/ar-no-strip
cat > %{__ar_no_strip} << EOF
#!/bin/sh
f=\$2
case \$(basename \$f) in
    *.a)
        ;;
    *)
        %{__strip} \$@
        ;;
esac
EOF
chmod +x %{__ar_no_strip}
%undefine __strip
%define __strip %{__ar_no_strip}

# Disable automatic requirements finding in %{cross_sysroot}
%define _use_internal_dependency_generator 0
%define __rpmdeps_command %{__find_requires}
%define __rpmdeps_skip_sysroot %{_builddir}/gcc-%{version}/rpmdeps-skip-sysroot
cat > %{__rpmdeps_skip_sysroot} << EOF
#!/bin/sh
while read oneline; do
    case \$oneline in
        %{buildroot}%{cross_sysroot}*)
            ;;
        *)
            echo \$oneline | %{__rpmdeps_command}
    esac
done
EOF
chmod +x %{__rpmdeps_skip_sysroot}
%undefine __find_requires
%define __find_requires %{__rpmdeps_skip_sysroot}


%files
%license COPYING COPYING.LIB COPYING.RUNTIME COPYING3 COPYING3.LIB
%doc ChangeLog ChangeLog.jit ChangeLog.tree-ssa MAINTAINERS NEWS README
%{_bindir}/%{cross_triplet}-cpp
%{_bindir}/%{cross_triplet}-gcc
%{_bindir}/%{cross_triplet}-gcc-ar
%{_bindir}/%{cross_triplet}-gcc-nm
%{_bindir}/%{cross_triplet}-gcc-ranlib
%{_bindir}/%{cross_triplet}-gcov
%{_bindir}/%{cross_triplet}-gcov-tool
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include-fixed/README
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include-fixed/limits.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include-fixed/syslimits.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stddef.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdarg.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdfix.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/varargs.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/float.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdbool.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/iso646.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdint.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdalign.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/stdatomic.h
%if %{cross_arch} == "arm"
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/mmintrin.h
%endif
%if %{cross_arch} == "arm" || %{cross_arch} == "arm64"
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/arm_acle.h
%endif
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/plugin
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/cc1
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/collect2
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/lto1
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/liblto_plugin.so*
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/plugin/gengtype
%if %{cross_stage} != "pass1"
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/unwind.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/crtbegin*.o
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/crtend*.o
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/crtfastmath.o
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libgcov.a
%{cross_sysroot}/%{lib_dir_name}/libgcc_s.so
%{cross_sysroot}/%{lib_dir_name}/libgcc_s.so.1
%endif
%if %{cross_stage} == "final"
%{_bindir}/%{cross_triplet}-c++
%{_bindir}/%{cross_triplet}-g++
%{_bindir}/%{cross_triplet}-gfortran
%dir %{_prefix}/%{cross_triplet}
%dir %{_prefix}/%{cross_triplet}/include
%dir %{_prefix}/%{cross_triplet}/include/c++
%{_prefix}/%{cross_triplet}/include/c++/%{version}
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/omp.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/openacc.h
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/objc
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/ssp
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/include/sanitizer
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/finclude
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/libcaf_single.a
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/cc1plus
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/cc1obj
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/cc1objplus
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/f951
%{cross_sysroot}/%{lib_dir_name}/libasan.a
%{cross_sysroot}/%{lib_dir_name}/libasan_preinit.o
%{cross_sysroot}/%{lib_dir_name}/libasan.so*
%{cross_sysroot}/%{lib_dir_name}/libatomic.a
%{cross_sysroot}/%{lib_dir_name}/libatomic.so*
%{cross_sysroot}/%{lib_dir_name}/libgfortran.a
%{cross_sysroot}/%{lib_dir_name}/libgfortran.so*
%{cross_sysroot}/%{lib_dir_name}/libgfortran.spec
%{cross_sysroot}/%{lib_dir_name}/libgomp.a
%{cross_sysroot}/%{lib_dir_name}/libgomp.so*
%{cross_sysroot}/%{lib_dir_name}/libgomp.spec
%{cross_sysroot}/%{lib_dir_name}/libitm.a
%{cross_sysroot}/%{lib_dir_name}/libitm.so*
%{cross_sysroot}/%{lib_dir_name}/libitm.spec
%{cross_sysroot}/%{lib_dir_name}/libobjc.a
%{cross_sysroot}/%{lib_dir_name}/libobjc.so*
%{cross_sysroot}/%{lib_dir_name}/libsanitizer.spec
%{cross_sysroot}/%{lib_dir_name}/libssp.a
%{cross_sysroot}/%{lib_dir_name}/libssp_nonshared.a
%{cross_sysroot}/%{lib_dir_name}/libssp.so
%{cross_sysroot}/%{lib_dir_name}/libssp.so.0*
%{cross_sysroot}/%{lib_dir_name}/libstdc++fs.a
%{cross_sysroot}/%{lib_dir_name}/libstdc++.a
%{cross_sysroot}/%{lib_dir_name}/libstdc++.so
%{cross_sysroot}/%{lib_dir_name}/libstdc++.so.6
%{cross_sysroot}/%{lib_dir_name}/libstdc++.so.6.*.*
%{cross_sysroot}/%{lib_dir_name}/libsupc++.a
%{cross_sysroot}/%{lib_dir_name}/libubsan.a
%{cross_sysroot}/%{lib_dir_name}/libubsan.so*
%if %{cross_arch} == "arm64"
%{cross_sysroot}/%{lib_dir_name}/liblsan.a
%{cross_sysroot}/%{lib_dir_name}/liblsan.so*
%{cross_sysroot}/%{lib_dir_name}/libtsan.a
%{cross_sysroot}/%{lib_dir_name}/libtsan.so*
%endif
%if %{enable_ada}
%{_bindir}/%{cross_triplet}-gnat
%{_bindir}/%{cross_triplet}-gnatbind
%{_bindir}/%{cross_triplet}-gnatchop
%{_bindir}/%{cross_triplet}-gnatclean
%{_bindir}/%{cross_triplet}-gnatfind
%{_bindir}/%{cross_triplet}-gnatkr
%{_bindir}/%{cross_triplet}-gnatlink
%{_bindir}/%{cross_triplet}-gnatls
%{_bindir}/%{cross_triplet}-gnatmake
%{_bindir}/%{cross_triplet}-gnatname
%{_bindir}/%{cross_triplet}-gnatprep
%{_bindir}/%{cross_triplet}-gnatxref
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/adainclude
%{_prefix}/lib/gcc/%{cross_triplet}/%{version}/adalib
%{_libexecdir}/gcc/%{cross_triplet}/%{version}/gnat1
%endif
%endif


%changelog
* Thu Dec 22 2016 Ting-Wei Lan <lantw44@gmail.com> - 6.3.0-1
- Update to new stable release 6.3.0

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 6.2.0-2
- Rebuilt for Fedora 25 and 26

* Thu Aug 25 2016 Ting-Wei Lan <lantw44@gmail.com> - 6.2.0-1
- Update to new stable release 6.2.0

* Sun May 08 2016 Ting-Wei Lan <lantw44@gmail.com> - 6.1.0-1
- Update to new stable release 6.1.0
- Drop support for Fedora 23 and older versions

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 5.3.0-3
- Rebuilt for Fedora 24 and 25

* Mon Dec 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.3.0-2
- Sync configure options with Fedora
- Support arm-linux-gnueabihf and aarch64-linux-gnu

* Sat Dec 05 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.3.0-1
- Update to new stable release 5.3.0
- Fix glibc build with dnf on Fedora 24

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-5
- Own the directory of C++ headers
- Require the filesystem sub-package

* Sun Nov 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-4
- Install license files and documentation

* Sat Nov 21 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-3
- Rebuilt for hardening flags

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-2
- Rebuilt for Fedora 23 and 24

* Fri Jul 17 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.2.0-1
- Update to new stable release 5.2.0

* Thu Apr 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.1.0-2
- Fix the usage of Fedora macro

* Wed Apr 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 5.1.0-1
- Update to new stable release 5.1.0
- Drop untested and possibly non-working Java support.
- Drop bundled CLooG because it is no longer required in GCC 5.
- Drop bundled ISL because it is now available in Fedora repository.
- Remove libcc1.so to prevent conflict with gcc-gdb-plugin.

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-4
- Rebuilt for Fedora 22 and 23
- Ada support cannot be built using GCC 5, so we disable it until GCC 5
  become a stable release.

* Fri Jan 02 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-3
- Enable Ada support on Fedora 21 or later.

* Sun Dec 21 2014 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-2
- Disable automatic requirements finding in %{cross_sysroot} instead of
  disabling it in all directories.
- Remove the %{cross_triplet}-kernel-headers dependency. It should be pulled
  in by %{cross_triplet}-glibc or %{cross_triplet}-glibc-headers.

* Fri Dec 19 2014 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-1
- Initial packaging
