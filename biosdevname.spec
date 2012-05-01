Name:		biosdevname
Version:	0.3.11
Release:	1%{?dist}
Summary:	Udev helper for naming devices per BIOS names

Group:		System Environment/Base
License:	GPLv2
URL:		http://linux.dell.com/files/%{name}
# SMBIOS only exists on these arches.  It's also likely that other
# arches don't expect the PCI bus to be sorted breadth-first, or of
# so, there haven't been any comments about that on LKML.
ExclusiveArch:	%{ix86} x86_64 ia64
Source0:	http://linux.dell.com/files/%{name}/permalink/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	pciutils-devel, zlib-devel
# to figure out how to name the rules file
BuildRequires:	udev
BuildRequires: automake autoconf
# for ownership of /etc/udev/rules.d
Requires: udev

Patch1: biosdevname-0.3.8-rules.patch

%description
biosdevname in its simplest form takes a kernel device name as an
argument, and returns the BIOS-given name it "should" be.  This is necessary
on systems where the BIOS name for a given device (e.g. the label on
the chassis is "Gb1") doesn't map directly and obviously to the kernel
name (e.g. eth0).

%prep
%setup -q
%patch1 -p1 -b .off 

%build
autoreconf
# this is a udev rule, so it needs to live in / rather than /usr
%configure --disable-rpath --prefix=/ --sbindir=/sbin
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install install-data DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README
/sbin/%{name}
# hack for either /etc or /lib rules location
/*/udev/rules.d/*.rules
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Sep 23 2011 Harald Hoyer <harald@redhat.com> 0.3.11-1
- version 0.3.11
Resolves: rhbz#736442
Resolves: rhbz#696252 rhbz#696203 rhbz#700248

* Tue Sep 20 2011 Harald Hoyer <harald@redhat.com> 0.3.10-1
- version 0.3.10
Resolves: rhbz#736442
Resolves: rhbz#696252 rhbz#696203 rhbz#700248

* Mon Jul 25 2011 Harald Hoyer <harald@redhat.com> 0.3.8-1
- version 0.3.8
Resolves: rhbz#696252 rhbz#696203 rhbz#700248

* Tue Apr 19 2011 Harald Hoyer <harald@redhat.com> 0.3.6-11
- change names for PCI add-in interfaces from pciXpY to pXpY
Resolves: rhbz#692820

* Tue Apr 12 2011 Harald Hoyer <harald@redhat.com> 0.3.6-10
- name NPAR capable devices correctly
Resolves: rhbz#692873

* Thu Mar 10 2011 Harald Hoyer <harald@redhat.com> 0.3.6-9
- restrict biosdevname to SMBIOS >= 2.6
Resolves: rhbz#653901

* Tue Mar 08 2011 Harald Hoyer <harald@redhat.com> 0.3.6-8
- only honor smbios settings
Resolves: rhbz#653901

* Thu Mar 03 2011 Harald Hoyer <harald@redhat.com> 0.3.6-7
- fix "false positives with PCI domains"
Resolves: rhbz#676932

* Tue Feb 15 2011 Harald Hoyer <harald@redhat.com> 0.3.6-6
- whitelist all Dell systems
Resolves: rhbz#653901

* Tue Feb 08 2011 Harald Hoyer <harald@redhat.com> 0.3.6-5
- don't use '#' in names, use 'p' instead, by popular demand
- fix segfault when BIOS advertises zero sized PIRQ Routing Table
- don't build and include dump_pirq
- add 'bonding' and 'openvswitch' to the virtual devices list
- fix test for PIRQ table version
Resolves: rhbz#653901

* Fri Jan 28 2011 Harald Hoyer <harald@redhat.com> 0.3.6-4
- use the new IMPORT{cmdline} feature to get the biosdevname
  kernel command line parameter
Resolves: rhbz#653901

* Wed Jan 26 2011 Harald Hoyer <harald@redhat.com> 0.3.6-3
- turn off biosdevname by default
  can be turned on by: udevadm control --property=UDEV_BIOSDEVNAME=1
  and retriggering the network devices
Resolves: rhbz#653901

* Wed Jan 26 2011 Harald Hoyer <harald@redhat.com> 0.3.6-2
- import into Red Hat Enterprise Linux
Resolves: rhbz#653901

* Tue Jan 25 2011 Matt Domsch <Matt_Domsch@dell.com> - 0.3.6-1
- drop biosdevnameS, it's unused and fails to build on F15

* Tue Jan 25 2011 Matt Domsch <Matt_Domsch@dell.com> - 0.3.5-1
- install dump_pirq into /usr/sbin
- fix udev rule, skip running if NAME is already set
- move udev rule to /lib/udev/rules.d by default

* Fri Jan 14 2011 Harald Hoyer <harald@redhat.com> 0.3.4-2
- import into Red Hat Enterprise Linux
Resolves: rhbz#653901

* Thu Dec 16 2010 Matt Domsch <mdomsch@fedoraproject.org> - 0.3.4-1
- drop unnecessary explicit version requirement on udev
- bugfix: start indices at 1 not 0, to match Dell and HP server port designations
- bugfix: don't assign names to unknown devices
- bugfix: don't assign duplicate names

* Thu Dec  9 2010 Matt Domsch <Matt_Domsch@dell.com> - 0.3.3-1
- add back in use of PCI IRQ Routing Table, if info is not provided by
  sysfs or SMBIOS

* Thu Dec  2 2010 Matt Domsch <Matt_Domsch@dell.com> - 0.3.2-1
- fix for multi-port cards with bridges
- removal of code for seriously obsolete systems

* Mon Nov 28 2010 Matt Domsch <Matt_Domsch@dell.com> 0.3.1-1
- remove all policies except 'physical' and 'all_ethN'
- handle SR-IOV devices properly

* Wed Nov 10 2010 Matt Domsch <Matt_Domsch@dell.com> 0.3.0-1
- add --policy=loms, make it default
- read index and labels from sysfs if available

* Mon Jul 27 2009 Jordan Hargrave <Jordan_Hargrave@dell.com> 0.2.5-1
- fix mmap error checking

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue May 06 2008 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-5
- use policy=all_names to find breakage

* Sun Feb 10 2008 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-4
- rebuild for gcc43

* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-3
- fix manpage entry in files
 
* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-2
- rebuild with Requires: udev > 115-3.20070920git

* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-1
- coordinate udev rules usage with udev maintainer
- fix crashes in pcmcia search, in_ethernet(), and incorrect command
  line parsing.

* Mon Aug 27 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.3-1
- eliminate libbiosdevname.*, pre and post scripts

* Fri Aug 24 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.2-1
- ExclusiveArch those arches with SMBIOS and PCI IRQ Routing tables
- eliminate libsysfs dependency, move app to / for use before /usr is mounted.
- build static

* Mon Aug 20 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.1-1
- initial release
