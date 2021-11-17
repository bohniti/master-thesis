#!/bin/bash

mkdir -p data

if [ ! -f linklist.txt ]
then
    START=1
    for PAGE in $( seq 1 200 ) # todo: replace 20 by 200
    do
        curl "https://quod.lib.umich.edu/a/apis?med=1;q1=inv;rgn1=ic_all;size=50;sort=m_flm;type=boolean;view=reslist;start=${START}" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'Referer: https://quod.lib.umich.edu/a/apis?med=1;size=50;sort=apis_inv;type=boolean;view=reslist;rgn1=ic_all;q1=inv' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Cookie: DLXSsid=11ddee0e0077ea39b197f6e4829e3327; STICKY=s147' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-User: ?1' \
            | grep '<a href' | grep 'apis/x' | grep '"img image"' | cut -d '"' -f 2 | tee -a linklist.txt
        START=$(( $START + 50 ))
        sleep $(( $RANDOM % 2 )).$(( ( $RANDOM % 10 ) + 1 ))s
    done
fi

if [ ! -f imglist.txt ]
then
    cat linklist.txt | while read LL
    do
        curl "$LL" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Cookie: DLXSsid=11ddee0e0077ea39b197f6e4829e3327; STICKY=s147' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: none' -H 'Sec-Fetch-User: ?1' -H 'Cache-Control: max-age=0' > foo
        IS_PAP=$( cat foo | grep -c '<dd class="pos1 last">Pap</dd>' )
        if [ $IS_PAP == 1 ]
        then
            URL=$( cat foo | grep 'image/api/image' | tail -n 1 | cut -d '"' -f 2 )
            echo "${LL}>https://quod.lib.umich.edu${URL}" | tee -a imglist.txt
        fi
        rm -f foo
        sleep 0.$(( ( $RANDOM % 10 ) + 1 ))s
    done
fi

cat imglist.txt | cut -d '>' -f 2 | sort -R | uniq | while read URL
do
    N=$( echo "$URL" | cut -d ':' -f 3,4 | tr ':' '_' | cut -d '.' -f 1 )
    wget -nc -O "data/${N}.jpg" "$URL"
    sleep $(( $RANDOM % 2 )).$(( ( $RANDOM % 10 ) + 1 ))s
done
