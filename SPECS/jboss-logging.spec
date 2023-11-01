%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:             jboss-logging
Version:          3.3.0
Release:          5%{?dist}
Summary:          The JBoss Logging Framework
License:          ASL 2.0
URL:              https://github.com/jboss-logging/jboss-logging
Source0:          https://github.com/jboss-logging/jboss-logging/archive/%{namedversion}.tar.gz
Patch0:           disable-log4j-backend.patch

BuildArch:        noarch

BuildRequires:    maven-local
BuildRequires:    mvn(log4j:log4j:12)
BuildRequires:    mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:    mvn(org.jboss:jboss-parent:pom:)
BuildRequires:    mvn(org.jboss.logmanager:jboss-logmanager)
BuildRequires:    mvn(org.slf4j:slf4j-api)

%description
This package contains the JBoss Logging Framework.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jboss-logging-%{namedversion}
%patch0 -p1

# Remove dependency on log4j 2.x - use 1.2
%pom_xpath_set pom:properties/pom:version.org.apache.log4j 12
%pom_remove_dep org.apache.logging.log4j:log4j-api
rm -f src/main/java/org/jboss/logging/Log4j2Logger{,Provider}.java

# SLF4j 1.7 upgrade
sed -i "s|map = MDC.getCopyOfContextMap();|map = (Map) MDC.getCopyOfContextMap();|" \
 src/main/java/org/jboss/logging/Slf4jLoggerProvider.java

# Unneeded task
%pom_remove_plugin :maven-source-plugin

cp -p src/main/resources/META-INF/LICENSE.txt .
sed -i 's/\r//' LICENSE.txt

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed May 30 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.0-5
- Disable log4j backend

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May 27 2016 gil cattaneo <puntogil@libero.it> 3.3.0-1
- update to 3.3.0.Final

* Sun Feb 14 2016 gil cattaneo <puntogil@libero.it> 3.1.4-6
- fix FTBFS rhbz#1307647
- fix BR list and use BR mvn()-like
- introduce license macro
- fix some rpmlint problem

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 01 2014 Marek Goldmann <mgoldman@redhat.com> - 3.1.4-3
- Upgrade to SLF4j 1.7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 14 2014 Marek Goldmann <mgoldman@redhat.com> - 3.1.4-1
- Upstream release 3.1.4.GA

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Marek Goldmann <mgoldman@redhat.com> - 3.1.3-1
- Upstream release 3.1.3.GA

* Tue Feb 26 2013 Marek Goldmann <mgoldman@redhat.com> - 3.1.2-1
- Upstream release 3.1.2.GA
- Move to mvn_build and mvn_install macros
- License change to ASL 2.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.1.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jul 20 2012 Marek Goldmann <mgoldman@redhat.com> - 3.1.0-4
- Fixed BR

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 26 2012 Marek Goldmann <mgoldman@redhat.com> 3.1.0-2
- Release bump

* Sun Feb 26 2012 Marek Goldmann <mgoldman@redhat.com> 3.1.0-1
- Upstream release 3.1.0.GA
- Relocated jars to _javadir

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-0.2.CR1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Marek Goldmann <mgoldman@redhat.com> 3.1.0-0.1.CR1
- Upstream release 3.1.0.CR1

* Mon Sep 19 2011 Marek Goldmann <mgoldman@redhat.com> 3.0.1-1
- Upstream release 3.0.1.GA

* Thu Jul 28 2011 Marek Goldmann <mgoldman@redhat.com> 3.0.0-1
- Initial packaging

