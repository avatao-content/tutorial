FROM avatao/tutorial:ragdoll-20201201

COPY solvable/supervisor /etc/supervisor
COPY solvable/webservice /home/user/webservice

RUN cd /home/user/webservice \
    && python3 -m pip install -r requirements.txt

VOLUME ["/home/user"]