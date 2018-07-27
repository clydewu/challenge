FROM debian:jessie

ARG APT_MIRROR=debian.csie.ntu.edu.tw 
ENV APT_MIRROR $APT_MIRROR

ARG MASKY_APP_PATH=/opt/pluvio/challenge/
ENV MASKY_APP_PATH $MASKY_APP_PATH

ARG MASKY_USER_NAME=masky
ENV MASKY_USER_NAME $MASKY_USER_NAME

ARG MASKY_USER_GROUP=masky
ENV MASKY_USER_GROUP $MASKY_USER_GROUP

ARG MASKY_USER_PASS=pluvio5278Clyde
ENV MASKY_USER_PASS $MASKY_USER_PASS

ARG DB_HOST
ENV DB_HOST $DB_HOST

ARG DB_PORT
ENV DB_PORT $DB_PORT

ARG DB_NAME
ENV DB_NAME $DB_NAME

ARG DB_COLLECTION
ENV DB_COLLECTION $DB_COLLECTION

#-- Set APT, use mirrors instead of origin offical source
RUN sed -i "s/deb.debian.org/$APT_MIRROR/g" /etc/apt/sources.list

#-- Add project folder
RUN mkdir -p $MASKY_APP_PATH

#-- Install based packages:
RUN apt-get update
RUN apt-get install -y vim build-essential sudo curl
RUN apt-get install -y python3 python3-dev build-essential libssl-dev apache2
RUN apt-get install -y apache2 libapache2-mod-wsgi-py3
RUN curl https://bootstrap.pypa.io/get-pip.py -o $MASKY_APP_PATH/get-pip.py
RUN python3 $MASKY_APP_PATH/get-pip.py

#-- Setup system users and groups
RUN useradd -d $MASKY_APP_PATH -G sudo -s /bin/bash $MASKY_USER_NAME \
&& echo "$MASKY_USER_NAME:$MASKY_USER_PASS" | chpasswd
RUN echo "alias python='python3'" >> $MASKY_APP_PATH/.profile

#-- Install pip requirement
COPY ./requirement.txt $MASKY_APP_PATH
RUN pip3 install -r $MASKY_APP_PATH/requirement.txt

#-- Copy application files and setup permission
COPY ./masky $MASKY_APP_PATH/masky
COPY ./masky.wsgi $MASKY_APP_PATH/
COPY ./fruits.csv $MASKY_APP_PATH/
COPY ./.flaskenv $MASKY_APP_PATH/

#-- Do migrate in entrypoint
COPY ./resources/entrypoint.sh /root/
RUN chmod +x /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]

#-- Setup services
COPY ./resources/000-masky.conf /etc/apache2/sites-enabled/000-masky.conf
RUN rm -f /etc/apache2/sites-enabled/000-default.conf

RUN chown -R "$MASKY_USER_NAME:$MASKY_USER_GROUP" $MASKY_APP_PATH

RUN apt-get clean all
RUN rm $MASKY_APP_PATH/get-pip.py

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

EXPOSE 80
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]