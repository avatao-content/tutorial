FROM avatao/tutorial:ragdoll-20210114


COPY solvable/webservice /home/user/webservice
COPY solvable/supervisor /etc/supervisor

RUN cd /home/user/webservice \
    && python3 -m pip install -r requirements.txt

RUN chown -R user:user /home/user/webservice

VOLUME ["/home/user"]