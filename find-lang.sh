#!/bin/sh
PROG=${0##*/}
if [ $# = 2 ]; then
	# for using same syntax as rpm own find-lang
	RPM_BUILD_ROOT=$1
	shift
fi
dir=$RPM_BUILD_ROOT/usr/share/roundcube
langfile=$1
tmp=$(mktemp) || exit 1
rc=0

lang_alias() {
	local lang=$1 l
	l=$(awk -F: -vl=$lang '$2 == l {print $1}' $0)
	echo ${l:-$lang}
}

find $dir -type d -name localization > $tmp

echo '%defattr(644,root,root,755)' > $langfile
while read dir; do
	echo "%dir ${dir#$RPM_BUILD_ROOT}" >> $langfile
	for path in $dir/*; do
		if [ -d "$path" ]; then
			lang=${path##*/}
			path=${path#$RPM_BUILD_ROOT}
		else
			lang=${path##*/}
			lang=${lang%.inc}
			path=${path#$RPM_BUILD_ROOT}
		fi

		lang=$(lang_alias "$lang")

		case "$lang" in
		index) # ignore
			continue
			;;
		*.*)
			echo >&2 "ERROR: Bad match: $lang"
			rc=1
		;;
		*-*)
			echo >&2 "ERROR: Need mapping for $lang!"
			rc=1
		;;
		en_US)
			lang=
			;;
		esac
		if [ "$lang" ]; then
			echo "%lang($lang) $path" >> $langfile
		else
			echo "$path" >> $langfile
		fi
	done
done < $tmp

if [ "$(grep -Ev '(^%defattr|^$)' $langfile | wc -l)" -le 0 ]; then
	echo >&2 "$PROG: Error: international files not found!"
	rc=1
fi

rm -f $tmp
exit $rc

# LANGMAP
az:az_AZ
bg:bg_BG
bs:bs_BA
ca:ca_ES
cs:cs_CZ
cy:cy_GB
da:da_DK
de:de_DE
el:el_GR
es:es_ES
et:et_EE
eu:eu_ES
fi:fi_FI
fr:fr_FR
ga:ga_IE
gl:gl_ES
he:he_IL
hi:hi_IN
hr:hr_HR
hu:hu_HU
hy:hy_AM
id:id_ID
is:is_IS
it:it_IT
ja:ja_JP
ka:ka_GE
ko:ko_KR
lt:lt_LT
lv:lv_LV
mk:mk_MK
mr:mr_IN
ms:ms_MY
nb:nb_NO
ne:ne_NP
nl:nl_NL
nn:nn_NO
pl:pl_PL
pt:pt_PT
ro:ro_RO
ru:ru_RU
si:si_LK
sk:sk_SK
sl:sl_SI
sq:sq_AL
sr:sr_CS
sv:sv_SE
th:th_TH
tr:tr_TR
uk:uk_UA
vn:vi_VN
