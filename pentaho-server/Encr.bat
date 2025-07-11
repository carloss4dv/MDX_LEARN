@echo off

REM *****************************************************************************
REM
REM Pentaho Data Integration
REM
REM Copyright (C) 2008 - 2022 by Hitachi Vantara : http://www.hitachivantara.com
REM
REM *****************************************************************************
REM
REM Licensed under the Apache License, Version 2.0 (the "License");
REM you may not use this file except in compliance with
REM the License. You may obtain a copy of the License at
REM
REM    http://www.apache.org/licenses/LICENSE-2.0
REM
REM Unless required by applicable law or agreed to in writing, software
REM distributed under the License is distributed on an "AS IS" BASIS,
REM WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
REM See the License for the specific language governing permissions and
REM limitations under the License.
REM
REM *****************************************************************************

setlocal
pushd %~dp0
SET STARTTITLE="Encr"
SET SPOON_CONSOLE=1
set JAVA_TOOL_OPTIONS=
java -cp tomcat/webapps/pentaho/WEB-INF/classes;tomcat/webapps/pentaho/WEB-INF/lib/pentaho-encryption-support-9.4.0.0-343.jar;tomcat/webapps/pentaho/WEB-INF/lib/jetty-util-9.4.18.v20190429.jar org.pentaho.support.encryption.Encr %*
popd
