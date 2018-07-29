FROM debian:jessie

ARG APT_MIRROR=debian.csie.ntu.edu.tw 
ENV APT_MIRROR $APT_MIRROR

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# -- Set APT, use mirrors instead of origin offical source
RUN sed -i "s/deb.debian.org/$APT_MIRROR/g" /etc/apt/sources.list

# -- Install based packages:
RUN apt-get update
RUN apt-get install -y vim build-essential sudo curl
RUN apt-get install -y python3 python3-dev build-essential libssl-dev apache2
RUN apt-get install -y apache2 libapache2-mod-wsgi-py3
RUN apt-get clean all

# -- Setup project folder
# Due to lacking template mechanism for other config file (e.g. apache conf)
# Please DO NOT overwrite MASKY_APP_PATH for now.
ARG MASKY_APP_PATH=/opt/pluvio/challenge/
ENV MASKY_APP_PATH $MASKY_APP_PATH

RUN mkdir -p $MASKY_APP_PATH

# -- Install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o $MASKY_APP_PATH/get-pip.py
RUN python3 $MASKY_APP_PATH/get-pip.py
RUN rm $MASKY_APP_PATH/get-pip.py

# -- Install pip requirement
COPY ./requirement.txt $MASKY_APP_PATH
RUN pip3 install -r $MASKY_APP_PATH/requirement.txt

# -- Setup system users and groups
ARG MASKY_USER_NAME=masky
ENV MASKY_USER_NAME $MASKY_USER_NAME

ARG MASKY_USER_GROUP=masky
ENV MASKY_USER_GROUP $MASKY_USER_GROUP

ARG MASKY_USER_PASS=pluvio5278Masky?
ENV MASKY_USER_PASS $MASKY_USER_PASS

RUN useradd -d $MASKY_APP_PATH -G sudo -s /bin/bash $MASKY_USER_NAME \
&& echo "$MASKY_USER_NAME:$MASKY_USER_PASS" | chpasswd
RUN echo "alias python='python3'" >> $MASKY_APP_PATH/.profile

# -- Setup configuration environment variables
ARG MASKY_DB_HOST
ENV MASKY_DB_HOST $MASKY_DB_HOST

ARG MASKY_DB_PORT
ENV MASKY_DB_PORT $MASKY_DB_PORT

ARG MASKY_DB_USERNAME
ENV MASKY_DB_USERNAME $MASKY_DB_USERNAME

ARG MASKY_DB_PASSWORD
ENV MASKY_DB_PASSWORD $MASKY_DB_PASSWORD

ARG MASKY_DB_NAME
ENV MASKY_DB_NAME $MASKY_DB_NAME

ARG MASKY_DB_COLLECTION
ENV MASKY_DB_COLLECTION $MASKY_DB_COLLECTION

# -- Copy application files
COPY ./masky $MASKY_APP_PATH/masky
COPY ./masky.wsgi $MASKY_APP_PATH/
COPY ./fruits.csv $MASKY_APP_PATH/
COPY ./.flaskenv $MASKY_APP_PATH/

# -- Setup entrypoint
COPY ./resources/entrypoint.sh /root/
RUN chmod +x /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]

# -- Setup apache
COPY ./resources/000-masky.conf /etc/apache2/sites-enabled/000-masky.conf
RUN rm -f /etc/apache2/sites-enabled/000-default.conf

# -- Setup permission
RUN chown -R "$MASKY_USER_NAME:$MASKY_USER_GROUP" $MASKY_APP_PATH

# -- Start apache
EXPOSE 80
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
