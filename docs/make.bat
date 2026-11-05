@ECHO OFF
REM Construcción de Sphinx en Windows: make.bat html  |  make.bat pdf

pushd %~dp0

if "%SPHINXBUILD%"=="" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build
set SPHINXPROJ=bohr-h-andresdperezc

if "%1"=="" goto help
if "%1"=="html" goto html
if "%1"=="pdf" goto pdf
if "%1"=="latexpdf" goto latexpdf
if "%1"=="clean" goto clean
goto other

:html
%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%/html %SPHINXOPTS%
goto end

:pdf
%SPHINXBUILD% -b rinoh %SOURCEDIR% %BUILDDIR%/rinoh %SPHINXOPTS%
goto end

:latexpdf
%SPHINXBUILD% -M latexpdf %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:clean
%SPHINXBUILD% -M clean %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:other
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
echo Uso: make.bat html ^| pdf ^| latexpdf ^| clean
echo Desde la raiz del proyecto tambien vale:
echo   sphinx-build -b html docs docs/_build/html
echo   sphinx-build -b rinoh docs docs/_build/rinoh

:end
popd
