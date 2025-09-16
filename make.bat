@echo off
SET CMD=%1

IF /i "%CMD%"=="test" (
	echo Executando testes...
	poetry run pytest
	goto :EOF
)

IF /i "%CMD%"=="lint" (
	echo Executando linter com ruff...
	poetry run ruff check --fix .
	goto :EOF
)

IF "%CMD%"=="format" (
	echo Formatando o codigo com black...
	poetry run black .
    goto :EOF
)

IF /i "%CMD%"=="check" (
	echo Verificando o codigo com ruff e black...
	poetry run ruff check .
	poetry run black --check .
	goto :EOF
)

echo Comando invalido: %CMD%
echo Uso: make [test] [lint] [format] [check]
