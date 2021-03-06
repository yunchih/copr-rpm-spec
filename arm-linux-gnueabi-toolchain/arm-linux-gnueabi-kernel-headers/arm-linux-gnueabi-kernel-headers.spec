%define cross_arch      arm
%define cross_triplet   arm-linux-gnueabi
%define cross_sysroot   %{_prefix}/%{cross_triplet}/sys-root

Name:       %{cross_triplet}-kernel-headers
Version:    4.9.7
Release:    1%{?dist}
Summary:    Header files for the Linux kernel (%{cross_triplet})

%define debug_package   %{nil}
%define kversion        %(echo %{version} | sed 's/\\.0$//')

Group:      Development/System
License:    GPLv2
URL:        https://www.kernel.org/
Source0:    https://www.kernel.org/pub/linux/kernel/v4.x/linux-%{kversion}.tar.xz

BuildRequires: %{cross_triplet}-filesystem
BuildRequires: perl
Requires:   %{cross_triplet}-filesystem

%description


%prep
%setup -qn linux-%{kversion}


%build
make ARCH=%{cross_arch} mrproper
make ARCH=%{cross_arch} headers_check


%install
install -d %{buildroot}%{cross_sysroot}
make headers_install ARCH=%{cross_arch} \
    INSTALL_HDR_PATH=%{buildroot}%{cross_sysroot}/usr
find %{buildroot}%{cross_sysroot} -name .install -delete
find %{buildroot}%{cross_sysroot} -name ..install.cmd -delete


%files
%dir %{cross_sysroot}/usr/include/asm
%{cross_sysroot}/usr/include/asm/*.h
%dir %{cross_sysroot}/usr/include/asm-generic
%{cross_sysroot}/usr/include/asm-generic/*.h
%dir %{cross_sysroot}/usr/include/drm
%{cross_sysroot}/usr/include/drm/*.h
%dir %{cross_sysroot}/usr/include/linux
%dir %{cross_sysroot}/usr/include/linux/android
%{cross_sysroot}/usr/include/linux/android/binder.h
%dir %{cross_sysroot}/usr/include/linux/byteorder
%{cross_sysroot}/usr/include/linux/byteorder/*.h
%dir %{cross_sysroot}/usr/include/linux/caif
%{cross_sysroot}/usr/include/linux/caif/*.h
%dir %{cross_sysroot}/usr/include/linux/can
%{cross_sysroot}/usr/include/linux/can/*.h
%dir %{cross_sysroot}/usr/include/linux/dvb
%{cross_sysroot}/usr/include/linux/dvb/*.h
%dir %{cross_sysroot}/usr/include/linux/hdlc
%{cross_sysroot}/usr/include/linux/hdlc/*.h
%dir %{cross_sysroot}/usr/include/linux/hsi
%{cross_sysroot}/usr/include/linux/hsi/*.h
%dir %{cross_sysroot}/usr/include/linux/iio
%{cross_sysroot}/usr/include/linux/iio/*.h
%dir %{cross_sysroot}/usr/include/linux/isdn
%{cross_sysroot}/usr/include/linux/isdn/*.h
%dir %{cross_sysroot}/usr/include/linux/mmc
%{cross_sysroot}/usr/include/linux/mmc/*.h
%dir %{cross_sysroot}/usr/include/linux/netfilter
%{cross_sysroot}/usr/include/linux/netfilter/*.h
%dir %{cross_sysroot}/usr/include/linux/netfilter/ipset
%{cross_sysroot}/usr/include/linux/netfilter/ipset/*.h
%dir %{cross_sysroot}/usr/include/linux/netfilter_arp
%{cross_sysroot}/usr/include/linux/netfilter_arp/*.h
%dir %{cross_sysroot}/usr/include/linux/netfilter_bridge
%{cross_sysroot}/usr/include/linux/netfilter_bridge/*.h
%dir %{cross_sysroot}/usr/include/linux/netfilter_ipv4
%{cross_sysroot}/usr/include/linux/netfilter_ipv4/*.h
%dir %{cross_sysroot}/usr/include/linux/netfilter_ipv6
%{cross_sysroot}/usr/include/linux/netfilter_ipv6/*.h
%dir %{cross_sysroot}/usr/include/linux/nfsd
%{cross_sysroot}/usr/include/linux/nfsd/*.h
%dir %{cross_sysroot}/usr/include/linux/raid
%{cross_sysroot}/usr/include/linux/raid/*.h
%dir %{cross_sysroot}/usr/include/linux/spi
%{cross_sysroot}/usr/include/linux/spi/*.h
%dir %{cross_sysroot}/usr/include/linux/sunrpc
%{cross_sysroot}/usr/include/linux/sunrpc/*.h
%dir %{cross_sysroot}/usr/include/linux/tc_act
%{cross_sysroot}/usr/include/linux/tc_act/*.h
%dir %{cross_sysroot}/usr/include/linux/tc_ematch
%{cross_sysroot}/usr/include/linux/tc_ematch/*.h
%dir %{cross_sysroot}/usr/include/linux/usb
%{cross_sysroot}/usr/include/linux/usb/*.h
%dir %{cross_sysroot}/usr/include/linux/wimax
%{cross_sysroot}/usr/include/linux/wimax/*.h
%dir %{cross_sysroot}/usr/include/linux
%{cross_sysroot}/usr/include/linux/*.h
%dir %{cross_sysroot}/usr/include/misc
%{cross_sysroot}/usr/include/misc/*.h
%dir %{cross_sysroot}/usr/include/mtd
%{cross_sysroot}/usr/include/mtd/*.h
%dir %{cross_sysroot}/usr/include/rdma
%{cross_sysroot}/usr/include/rdma/*.h
%dir %{cross_sysroot}/usr/include/rdma/hfi
%{cross_sysroot}/usr/include/rdma/hfi/hfi1_user.h
%dir %{cross_sysroot}/usr/include/scsi
%{cross_sysroot}/usr/include/scsi/*.h
%dir %{cross_sysroot}/usr/include/scsi/fc
%{cross_sysroot}/usr/include/scsi/fc/*.h
%dir %{cross_sysroot}/usr/include/sound
%{cross_sysroot}/usr/include/sound/*.h
%dir %{cross_sysroot}/usr/include/video
%{cross_sysroot}/usr/include/video/*.h
%dir %{cross_sysroot}/usr/include/xen
%{cross_sysroot}/usr/include/xen/*.h


%changelog
* Thu Feb 02 2017 Ting-Wei Lan <lantw44@gmail.com> - 4.9.7-1
- Update to 4.9.7

* Fri Jan 27 2017 Ting-Wei Lan <lantw44@gmail.com> - 4.9.6-1
- Update to 4.9.6

* Fri Jan 20 2017 Ting-Wei Lan <lantw44@gmail.com> - 4.9.5-1
- Update to 4.9.5

* Mon Jan 16 2017 Ting-Wei Lan <lantw44@gmail.com> - 4.9.4-1
- Update to 4.9.4

* Fri Jan 13 2017 Ting-Wei Lan <lantw44@gmail.com> - 4.9.3-1
- Update to 4.9.3

* Mon Jan 09 2017 Ting-Wei Lan <lantw44@gmail.com> - 4.9.2-1
- Update to 4.9.2

* Fri Jan 06 2017 Ting-Wei Lan <lantw44@gmail.com> - 4.9.1-1
- Update to 4.9.1

* Mon Dec 12 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.9.0-1
- Update to 4.9

* Mon Dec 12 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.14-1
- Update to 4.8.14

* Fri Dec 09 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.13-1
- Update to 4.8.13

* Sat Dec 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.12-1
- Update to 4.8.12

* Thu Dec 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.11-1
- Update to 4.8.11

* Tue Nov 22 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.10-1
- Update to 4.8.10

* Sat Nov 19 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.9-1
- Update to 4.8.9

* Wed Nov 16 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.8-1
- Update to 4.8.8

* Fri Nov 11 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.7-1
- Update to 4.8.7

* Tue Nov 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.6-1
- Update to 4.8.6

* Fri Oct 28 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.5-1
- Update to 4.8.5

* Sat Oct 22 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.4-1
- Update to 4.8.4

* Thu Oct 20 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.3-1
- Update to 4.8.3

* Wed Oct 19 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.2-1
- Update to 4.8.2

* Sat Oct 08 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.1-1
- Update to 4.8.1

* Mon Oct 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.8.0-1
- Update to 4.8

* Fri Sep 30 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.7.6-1
- Update to 4.7.6

* Sat Sep 24 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.7.5-1
- Update to 4.7.5

* Thu Sep 15 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.7.4-1
- Update to 4.7.4

* Sat Sep 10 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.7.3-2
- Rebuilt for Fedora 25 and 26

* Wed Sep 07 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.7.3-1
- Update to 4.7.3

* Thu Aug 25 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.7.2-1
- Update to 4.7.2

* Fri Aug 19 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.7.1-1
- Update to 4.7.1

* Mon Jul 25 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.7.0-1
- Update to 4.7
- Perl have to be listed in BuildRequires on Fedora 25

* Tue Jul 12 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.6.4-1
- Update to 4.6.4

* Sun Jun 26 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.6.3-1
- Update to 4.6.3

* Thu Jun 09 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.6.2-1
- Update to 4.6.2

* Thu Jun 02 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.6.1-1
- Update to 4.6.1

* Mon May 16 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.6.0-1
- Update to 4.6

* Thu May 12 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.5.4-1
- Update to 4.5.4

* Thu May 05 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.5.3-1
- Update to 4.5.3

* Thu Apr 21 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.5.2-1
- Update to 4.5.2

* Thu Apr 14 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.5.1-1
- Update to 4.5.1

* Tue Mar 15 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.5.0-1
- Update to 4.5

* Sun Mar 13 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.4.5-1
- Update to 4.4.5

* Fri Mar 04 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.4.4-1
- Update to 4.4.4

* Thu Mar 03 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.4.3-2
- Rebuilt for Fedora 24 and 25

* Sat Feb 27 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.4.3-1
- Update to 4.4.3

* Thu Feb 18 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.4.2-1
- Update to 4.4.2

* Mon Feb 01 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.4.1-1
- Update to 4.4.1

* Mon Jan 11 2016 Ting-Wei Lan <lantw44@gmail.com> - 4.4.0-1
- Update to 4.4

* Fri Dec 11 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.3.3-1
- Update to 4.3.3

* Fri Dec 11 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.3.2-1
- Update to 4.3.2

* Fri Dec 11 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.3.1-1
- Update to 4.3.1

* Tue Nov 24 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.3.0-2
- Own all directories
- Require the filesystem sub-package

* Mon Nov 02 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.3.0-1
- Update to 4.3

* Tue Oct 27 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.2.5-1
- Update to 4.2.5

* Fri Oct 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.2.4-1
- Update to 4.2.4

* Sat Oct 03 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.2.3-1
- Update to 4.2.3

* Wed Sep 30 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.2.2-1
- Update to 4.2.2

* Tue Sep 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.2.1-2
- Disable debuginfo package because RPM 4.13 does not allow empty debuginfo
  package. This fixes the build on Fedora 23 and 24.

* Tue Sep 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.2.1-1
- Update to 4.2.1

* Mon Aug 31 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.2.0-1
- Update to 4.2

* Tue Aug 18 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.6-1
- Update to 4.1.6

* Tue Aug 11 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.5-1
- Update to 4.1.5

* Tue Aug 04 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.4-1
- Update to 4.1.4

* Tue Jul 28 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.3-2
- Rebuilt for Fedora 23 and 24

* Wed Jul 22 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.3-1
- Update to 4.1.3

* Sun Jul 12 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.2-1
- Update to 4.1.2

* Wed Jul 01 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.1-1
- Update to 4.1.1

* Tue Jun 23 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.1.0-1
- Update to 4.1

* Sun Jun 07 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.5-1
- Update to 4.0.5

* Tue May 19 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.4-1
- Update to 4.0.4

* Thu May 14 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.3-1
- Update to 4.0.3

* Thu May 07 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.2-1
- Update to 4.0.2

* Thu Apr 30 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.1-1
- Update to 4.0.1

* Mon Apr 13 2015 Ting-Wei Lan <lantw44@gmail.com> - 4.0.0-1
- Update to 4.0

* Thu Mar 26 2015 Ting-Wei Lan <lantw44@gmail.com> - 3.19.3-1
- Update to 3.19.3

* Fri Mar 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 3.19.2-2
- Update to 3.19.2

* Sun Mar 15 2015 Ting-Wei Lan <lantw44@gmail.com> - 3.19.1-1
- Update to 3.19.1

* Thu Dec 18 2014 Ting-Wei Lan <lantw44@gmail.com> - 3.18.1-1
- Initial packaging
