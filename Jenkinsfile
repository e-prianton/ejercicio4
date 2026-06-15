pipeline {
    agent any

    environment {
        GIT_REPO           = 'https://github.com/e-prianton/ejercicio4.git'
        DEVELOP_BRANCH     = 'develop'
        WORKING_BRANCH     = 'WorkingBranch'
        GIT_CREDENTIALS    = '01'
    }

    triggers {
        // Al no tener webhook, Jenkins comprueba cambios cada minuto
        pollSCM('* * * * *')
    }

    stages {

        // ══════════════════════════════════════
        // STAGE 1 — MERGE EN LOCAL
        // ══════════════════════════════════════
        stage('Merge en local') {
            steps {
                echo ">>> Clonando rama ${DEVELOP_BRANCH}..."
                git(
                    url: env.GIT_REPO,
                    branch: env.DEVELOP_BRANCH,
                    credentialsId: env.GIT_CREDENTIALS
                )

                echo ">>> Haciendo merge de ${WORKING_BRANCH} sobre ${DEVELOP_BRANCH}..."
                sh '''
                    git fetch origin
                    git checkout develop
                    git merge origin/WorkingBranch --no-ff --no-commit
                    echo "Merge completado sin conflictos."
                '''
            }
            post {
                failure {
                    echo "ERROR: Conflictos en el merge. Pipeline abortada."
                }
            }
        }

        // ══════════════════════════════════════
        // STAGES 2 y 3 — PARALELO
        // Compilación + Tests unitarios
        // ══════════════════════════════════════
        stage('Compilacion y Tests en paralelo') {
            parallel {

                // ── STAGE 2: Compilación ──
                stage('Compilacion') {
                    steps {
                        echo ">>> Iniciando compilación del código de producción..."
                        // Sustituir por: sh 'make build' / sh 'mvn compile' / sh 'gradle build'
                        sh '''
                            echo "Compilando..."
                            sleep 2
                            echo "Compilación completada OK."
                        '''
                    }
                    post {
                        success { echo "Compilación exitosa." }
                        failure { echo "ERROR: Fallo en compilación." }
                    }
                }

                // ── STAGE 3: Tests unitarios ──
                stage('Tests unitarios') {
                    steps {
                        echo ">>> Ejecutando tests unitarios..."
                        // Sustituir por: sh 'pytest tests/' / sh 'mvn test' / sh 'gradle test'
                        sh '''
                            echo "Ejecutando tests..."
                            sleep 2
                            echo "Todos los tests pasaron OK."
                        '''
                    }
                    post {
                        success { echo "Tests superados." }
                        failure { echo "ERROR: Tests fallidos." }
                    }
                }

            } // fin parallel
        } // fin stage paralelo

    } // fin stages

    // ══════════════════════════════════════
    // POST — Resultado global
    // ══════════════════════════════════════
    post {
        success {
            echo "Pipeline completada con exito. Merge request aprobado."
        }
        failure {
            echo "Pipeline fallida. Merge request bloqueado."
        }
        always {
            cleanWs()
        }
    }

}
