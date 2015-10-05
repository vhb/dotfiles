#-
# Copyright 2013-2014 Emmanuel Vadot <elbarto@bocal.org>
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions 
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

Name:           ns_auth
Version:	1.3
Release:	2
License:        BSD-2-Clause
Summary:        Simple netsoul client
BuildRequires:	python3
BuildArch:      noarch
Source0:        ftp://ftp.bocal.org/pub/%{name}/%{version}/%{name}-%{version}.tgz
Vendor:		Bocal
Url:            http://www.bocal.org
Group:          Applications/Internet
Packager:       Emmanuel Vadot <elbarto@bocal.org>

%description
Simple netsoul client

%prep
%setup

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp %{name}.py %{buildroot}%{_bindir}/%{name}

%files
%attr(755,root,root) %{_bindir}/%{name}

%changelog
* Fri Feb 28 2014 Emmanuel Vadot <elbarto@bocal.org> - 1.3-2
- change arch to noarch
- change licence to BSD-2-Clause
- change group to Applications/Internet
