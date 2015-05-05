%define revcount %(git rev-list HEAD | wc -l)
%define treeish %(git rev-parse --short HEAD)
%define localmods %(git diff-files --exit-code --quiet  || date +.m%%j%%H%%M%%S)

%define srcdir   %{getenv:PWD}

Summary: Redgate Base OS Configuration
Name: redgate-os-config
Version: 1.0
Release: %{revcount}.%{treeish}%{localmods}
Distribution: Redgate
Group: System Environment/Daemons
License: Proprietary
Packager: Karl Redgate <Karl.Redgate@gmail.com>
BuildArch: noarch
Requires: cronie
Requires: upstart
Requires: rsyslog
Requires: logrotate
Requires: filesystem
# Requires: anaconda
Requires: dracut
Requires: kernel
Requires: chkconfig
# Requires: NetworkManager
# Requires: crash
Requires: gettext
# Requires: lm_sensors
Requires: patch
Requires: sysfsutils
# Requires: sharutils
# Requires: wireshark
# Requires: ruby-irb
# Requires: dhcp
# Requires: libcgroup
# Requires: libvirt
# Requires: qemu-kvm
# for shasum - used in tool to reset rabbitmq server
Requires: perl-Digest-SHA
Requires: telnet


%define _topdir %(echo $PWD)/rpm
BuildRoot: %{_topdir}/BUILDROOT
%define Exports %(echo $PWD)/exports

# Require utilities used and those that provide files modified by %post.
# This would be better handled by using %triggerin scripts to support OS update.
Requires(post): chkconfig
Requires(post): initscripts

%description
Scripts, etc, for configuring base OS/Distro.

%prep
%build

%install

DIR_ARGS=" -d --mode=755 "
DATA_ARGS=" --mode=644 "
PROG_ARGS=" --mode=755 "

%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/sysconfig/redgate
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/modprobe.d
%{__install} $DATA_ARGS %{srcdir}/etc/modprobe.d/*.conf $RPM_BUILD_ROOT/etc/modprobe.d
# Install sysctl config
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/sysctl.d
%{__install} $DATA_ARGS %{srcdir}/etc/sysctl.d/* $RPM_BUILD_ROOT/etc/sysctl.d
# Install init/upstart config
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/init/redgate/configure
%{__install} $DATA_ARGS %{srcdir}/etc/init/*.conf $RPM_BUILD_ROOT/etc/init
%{__install} $DATA_ARGS %{srcdir}/etc/init/redgate/*.conf $RPM_BUILD_ROOT/etc/init/redgate
#%{__install} $DATA_ARGS %{srcdir}/etc/init/redgate/configure/* $RPM_BUILD_ROOT/etc/init/redgate/configure
#%{__install} $DIR_ARGS $RPM_BUILD_ROOT/usr/sbin
#%{__install} $PROG_ARGS %{srcdir}/usr/sbin/* $RPM_BUILD_ROOT/usr/sbin
# add the rsyslog config
#%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/rsyslog.d
#%{__install} $DATA_ARGS %{srcdir}/etc/rsyslog-redgate.conf $RPM_BUILD_ROOT/etc
# add halt config directory
#%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/halt.d
#%{__install} $PROG_ARGS %{srcdir}/etc/halt.d/H* $RPM_BUILD_ROOT/etc/halt.d
# add cron configuration
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/cron.d
%{__install} $DATA_ARGS %{srcdir}/etc/cron.d/* $RPM_BUILD_ROOT/etc/cron.d
# add logrotate hourly
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/cron.hourly
%{__install} $PROG_ARGS %{srcdir}/etc/cron.hourly/* $RPM_BUILD_ROOT/etc/cron.hourly
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/cron.daily
%{__install} $PROG_ARGS %{srcdir}/etc/cron.daily/* $RPM_BUILD_ROOT/etc/cron.daily
#%{__install} $PROG_ARGS %{srcdir}/etc/logrotate.hourly.conf $RPM_BUILD_ROOT/etc
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/usr/libexec/redgate
%{__install} $PROG_ARGS %{srcdir}/usr/libexec/redgate/* $RPM_BUILD_ROOT/usr/libexec/redgate
# sbin tools
#%{__install} $DIR_ARGS $RPM_BUILD_ROOT/sbin
#%{__install} $PROG_ARGS %{srcdir}/sbin/* $RPM_BUILD_ROOT/sbin
# custom syslog rotation
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/logrotate.d
%{__install} $DATA_ARGS %{srcdir}/etc/logrotate.d/* $RPM_BUILD_ROOT/etc/logrotate.d
# ldconfig
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/ld.so.conf.d
%{__install} $DATA_ARGS %{srcdir}/etc/ld.so.conf.d/* $RPM_BUILD_ROOT/etc/ld.so.conf.d
# override system logrotate.conf
#%{__install} $DATA_ARGS %{srcdir}/etc/logrotate.conf $RPM_BUILD_ROOT/etc/logrotate.conf.stratus
# install branded boot splash screen
#%{__install} $DIR_ARGS $RPM_BUILD_ROOT/boot/grub
#%{__install} $DATA_ARGS %{srcdir}/boot/grub/redgate-splash.xpm.gz $RPM_BUILD_ROOT/boot/grub/

# Redis config
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/etc/redis/
%{__install} $DATA_ARGS %{srcdir}/etc/redis/* $RPM_BUILD_ROOT/etc/redis/

%{__install} $DIR_ARGS $RPM_BUILD_ROOT/var/log/redgate
%{__install} $DIR_ARGS $RPM_BUILD_ROOT/var/run/redgate

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
/etc/sysconfig/redgate/
/etc/init/
/etc/cron.d/
/etc/cron.hourly/
/etc/cron.daily/
/etc/logrotate.d/
/etc/modprobe.d/
/etc/sysctl.d/
/etc/ld.so.conf.d/
# /etc/rsyslog.d/
# /etc/rsyslog-redgate.conf
# /usr/sbin/
/usr/libexec/
# /etc/halt.d/
# /sbin/
# /boot/
/etc/redis/redgate.conf
%attr(775,redgate,redgate) /var/run/redgate
%attr(775,redgate,redgate) /var/log/redgate

%post
[ "$1" -gt 1 ] && {
    : Upgrading
}

[ "$1" = 1 ] && {
    : New install
}

/usr/libexec/redgate/update-dmi-info
/usr/libexec/redgate/create-users

ldconfig

# [ -f /boot/grub/redgate-splash.xpm.gz ] && mv -f /boot/grub/redgate-splash.xpm.gz /boot/grub/splash.xpm.gz

# /sbin/chkconfig --level 12345 rsyslog off

: Done

%triggerin -- firstboot
# Disable firstboot any time it gets installed or upgraded
/sbin/chkconfig --level 12345 firstboot off

%triggerin -- redis
# Disable firstboot any time it gets installed or upgraded
/sbin/chkconfig --level 12345 redis off

%changelog

* Sun Nov 24 2013 Karl Redgate <www.redgates.com>
- Initial build

# vim:autoindent expandtab sw=4
