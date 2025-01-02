Name:		fermilab-conf_email-gateway
Version:	1.1
Release:	5%{?dist}
Summary:	Configure postfix to use the FNAL email gateway

%if 0%{?rhel} < 10
Obsoletes:	zz_postfix_fermi_gateway
%endif

Group:		Fermilab
License:	GPL
URL:		https://github.com/fermilab-context-rpms/fermilab-conf_email-gateway

BuildArch:	noarch

Requires(post):	systemd

%description
Email sent from Fermilab's network must route through an authorized SMTP server.
This rpm will configure postfix to utilize an authorized gateway.

See: KB0010765
%prep


%build


%install


%files
%defattr(0644,root,root,0755)

#####################################################################
%triggerin -p /bin/bash -- postfix 

##################### BEGIN Trigger Snippet #########################
set -u
TRIGGER_ON_PACKAGE_NAME='postfix'
# The following script snippet attempts to classify why we were called:
#  - on first install of either package, RUN_TRIGGER == "Initial"
#  - on upgrade of _THIS_ package, RUN_TRIGGER == "UpgradeSELF"
#  - on upgrade of the TRIGGERON package, RUN_TRIGGER == "UpgradeTRIGGERON"
#  - on upgrade of the TRIGGERON package but initial install of _THIS_ package, RUN_TRIGGER == "InitialSELFUpgradeTRIGGERON"
#  - on upgrade of the BOTH packages, RUN_TRIGGER == "UPGRADEALL"

CURRENT_INSTALLS_OF_THIS_PACKAGE=${1:-0}
TRIGGER_ON_PACKAGE=${2:-0}

RUN_TRIGGER="NO"
if [[ ${TRIGGER_ON_PACKAGE} -eq 1 ]]; then
    # We only get here if we are NOT doing an upgrade of the trigger package
    if [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 0 ]]; then
        # We only get here if we are removing _THIS_ package
        RUN_TRIGGER="UninstallSELF"
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 1 ]]; then
        # We only get here if we are NOT doing an upgrade of the trigger package
        #                and we are installing _THIS_ package for the first time
        RUN_TRIGGER="Initial"
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -gt 1 ]]; then
        # We only get here if we are NOT doing an upgrade of the trigger package
        #                and we are upgrading _THIS_ package
        RUN_TRIGGER="UpgradeSELF"
    fi
elif [[ ${TRIGGER_ON_PACKAGE} -gt 1 ]]; then
    # We only get here if we are doing an upgrade of the trigger package
    if [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 1 ]]; then
        # We get here if we are doing an upgrade of the trigger package
        #                     and we are NOT upgrading _THIS_ package
        RUN_TRIGGER="UpgradeTRIGGERON"

        #  But, are we installing _THIS_ package as a part of a dependency
        #       resolution chain?
        _THIS_TID=$(rpm -q --qf "%{INSTALLTID}\n" %{NAME})
        # Find the last installed (ie the current) TRIGGER_ON_PACKAGE_NAME's transaction
        TID=$(rpm -q --qf "%{INSTALLTID}\n" ${TRIGGER_ON_PACKAGE_NAME} --last |grep -v ${TRIGGER_ON_PACKAGE_NAME} | head -1)
        if [[ "${_THIS_TID}" == "${TID}" ]]; then
            # if the transaction ID of _THIS_ package is identical to the
            #  transaction ID of an installed TRIGGER_ON_PACKAGE_NAME
            # then, we must be upgrading the trigger package and
            # installing _THIS_ package
            RUN_TRIGGER="InitialSELFUpgradeTRIGGERON"
        fi
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -gt 1 ]]; then
        # We only get here if we are doing an upgrade of the trigger package
        #                     and we are upgrading _THIS_ package
        RUN_TRIGGER="UpgradeALL"
    fi
elif [[ ${TRIGGER_ON_PACKAGE} -eq 0 ]]; then
    # We only get here if we are removing the trigger package
    RUN_TRIGGER="UninstallTRIGGERON"
fi

if [[ "${RUN_TRIGGER}" == "NO" ]]; then
    # If we got here if:
    #  some kind of edge case appeared......
    echo "##################################" >&2
    echo "%{NAME}: Not sure what this means"  >&2
    echo "CURRENT_INSTALLS_OF_THIS_PACKAGE = ${CURRENT_INSTALLS_OF_THIS_PACKAGE}"  >&2
    echo "TRIGGER_ON_PACKAGE (${TRIGGER_ON_PACKAGE_NAME}) = ${TRIGGER_ON_PACKAGE}" >&2
    echo "##################################" >&2
    exit 1
fi

##################### End of Trigger Snippet ########################

if [[ "${RUN_TRIGGER}" == "UpgradeTRIGGERON" ]]; then
    # If we got here if:
    #  a) we are upgrading the trigger package, but not _THIS_ package
    #       so we've already run this once and will not run it again.
    exit 0
fi


# sane defaults for "everyone"
postconf -e inet_interfaces=localhost
postconf -e inet_protocols=all
postconf -e 'mynetworks=127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128'
postconf -e 'mydestination=$myorigin, localhost.$mydomain, localhost'
postconf -e smtp_tls_security_level=may

# FNAL specifics
postconf -e mydomain=fnal.gov
#postconf -e 'masquerade_domains=$mydomain'
#postconf -e 'masquerade_classes=envelope_sender'
postconf -e 'relayhost=[smtp.fnal.gov]:587'

systemctl condrestart postfix.service
#####################################################################

#####################################################################
%triggerun -p /bin/bash -- postfix 

##################### BEGIN Trigger Snippet #########################
set -u
TRIGGER_ON_PACKAGE_NAME='postfix'
# The following script snippet attempts to classify why we were called:
#  - on first install of either package, RUN_TRIGGER == "Initial"
#  - on upgrade of _THIS_ package, RUN_TRIGGER == "UpgradeSELF"
#  - on upgrade of the TRIGGERON package, RUN_TRIGGER == "UpgradeTRIGGERON"
#  - on upgrade of the TRIGGERON package but initial install of _THIS_ package, RUN_TRIGGER == "InitialSELFUpgradeTRIGGERON"
#  - on upgrade of the BOTH packages, RUN_TRIGGER == "UPGRADEALL"

CURRENT_INSTALLS_OF_THIS_PACKAGE=${1:-0}
TRIGGER_ON_PACKAGE=${2:-0}

RUN_TRIGGER="NO"
if [[ ${TRIGGER_ON_PACKAGE} -eq 1 ]]; then
    # We only get here if we are NOT doing an upgrade of the trigger package
    if [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 0 ]]; then
        # We only get here if we are removing _THIS_ package
        RUN_TRIGGER="UninstallSELF"
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 1 ]]; then
        # We only get here if we are NOT doing an upgrade of the trigger package
        #                and we are installing _THIS_ package for the first time
        RUN_TRIGGER="Initial"
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -gt 1 ]]; then
        # We only get here if we are NOT doing an upgrade of the trigger package
        #                and we are upgrading _THIS_ package
        RUN_TRIGGER="UpgradeSELF"
    fi
elif [[ ${TRIGGER_ON_PACKAGE} -gt 1 ]]; then
    # We only get here if we are doing an upgrade of the trigger package
    if [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -eq 1 ]]; then
        # We get here if we are doing an upgrade of the trigger package
        #                     and we are NOT upgrading _THIS_ package
        RUN_TRIGGER="UpgradeTRIGGERON"

        #  But, are we installing _THIS_ package as a part of a dependency
        #       resolution chain?
        _THIS_TID=$(rpm -q --qf "%{INSTALLTID}\n" %{NAME})
        # Find the last installed (ie the current) TRIGGER_ON_PACKAGE_NAME's transaction
        TID=$(rpm -q --qf "%{INSTALLTID}\n" ${TRIGGER_ON_PACKAGE_NAME} --last |grep -v ${TRIGGER_ON_PACKAGE_NAME} | head -1)
        if [[ "${_THIS_TID}" == "${TID}" ]]; then
            # if the transaction ID of _THIS_ package is identical to the
            #  transaction ID of an installed TRIGGER_ON_PACKAGE_NAME
            # then, we must be upgrading the trigger package and
            # installing _THIS_ package
            RUN_TRIGGER="InitialSELFUpgradeTRIGGERON"
        fi
    elif [[ ${CURRENT_INSTALLS_OF_THIS_PACKAGE} -gt 1 ]]; then
        # We only get here if we are doing an upgrade of the trigger package
        #                     and we are upgrading _THIS_ package
        RUN_TRIGGER="UpgradeALL"
    fi
elif [[ ${TRIGGER_ON_PACKAGE} -eq 0 ]]; then
    # We only get here if we are removing the trigger package
    RUN_TRIGGER="UninstallTRIGGERON"
fi

if [[ "${RUN_TRIGGER}" == "NO" ]]; then
    # If we got here if:
    #  some kind of edge case appeared......
    echo "##################################" >&2
    echo "%{NAME}: Not sure what this means"  >&2
    echo "CURRENT_INSTALLS_OF_THIS_PACKAGE = ${CURRENT_INSTALLS_OF_THIS_PACKAGE}"  >&2
    echo "TRIGGER_ON_PACKAGE (${TRIGGER_ON_PACKAGE_NAME}) = ${TRIGGER_ON_PACKAGE}" >&2
    echo "##################################" >&2
    exit 1
fi

##################### End of Trigger Snippet ########################

if [[ "${RUN_TRIGGER}" != "UninstallSELF" ]]; then
    # If we got here if:
    #  a) we are not uninstalling _THIS_ package
    exit 0
fi


# # #
postconf -n mydomain | grep -q fnal.gov
if [[ $? -eq 0 ]]; then
    postconf -X mydomain
    #postconf -X masquerade_domains || :
    #postconf -X masquerade_classes || :
fi
postconf -n relayhost |grep -q smtp.fnal.gov
if [[ $? -eq 0 ]]; then
    postconf -X relayhost
fi
systemctl condrestart postfix.service
#####################################################################


#####################################################################
#####################################################################
%changelog
* Fri Apr 15 2022 Pat Riehecky <riehecky@fnal.gov> 1.1-5
- Disable masquerade_domains

* Mon Feb 21 2022 Pat Riehecky <riehecky@fnal.gov> 1.1-4
- Prep for IPv6 and full TLS
- Setup masquerade_domains

* Mon Nov 2 2015 Pat Riehecky <riehecky@fnal.gov> 1.1-3
- Now removes config during uninstall

* Wed Sep 9 2015 Pat Riehecky <riehecky@fnal.gov> 1.1-2.1
- Fixed typo

* Fri Sep 4 2015 Pat Riehecky <riehecky@fnal.gov> 1.1-2
- updated requires list

* Fri Aug 7 2015 Pat Riehecky <riehecky@fnal.gov> 1.1-1
- Initial build for EL7
