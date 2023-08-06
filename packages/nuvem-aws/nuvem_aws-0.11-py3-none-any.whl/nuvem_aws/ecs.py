import subprocess
import os
import json
import traceback
import time
import re

class ECS:
  def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, aws_account_id, cluster, task, security_group, subnet):
    self.aws_access_key_id = aws_access_key_id
    self.aws_secret_access_key = aws_secret_access_key
    self.aws_region = aws_region
    self.aws_account_id = aws_account_id
    self.cluster = cluster
    self.security_group = security_group
    self.subnet = subnet
    self.task = task
    self.valido = False
    self.lista_de_clusters = {}

  def check_subnet(self):
    retorno = True

    try:
      os.environ['AWS_ACCESS_KEY_ID'] = self.aws_access_key_id
      os.environ['AWS_SECRET_ACCESS_KEY'] = self.aws_secret_access_key
      os.environ['AWS_REGION'] = self.aws_region
      snt_cmd = 'aws ec2 describe-subnets --filter "Name=subnet-id,Values={0}" --output json'.format(self.subnet)
      p = subprocess.run(snt_cmd, shell = True, capture_output = True)
      o = p.stdout.decode()
      e = p.stderr.decode()

      if p.returncode > 0:
        retorno = False
      else:
        if p.stderr.decode() == '':
          t = json.loads(p.stdout.decode())
          retorno = len(t.get('Subnets')) > 0
        else:
          retorno = False
          print(p.stderr.decode())
    except Exception as e:
      retorno = False
      print(traceback.format_exc())

    return retorno

  def check_security_group(self):
    retorno = True

    try:
      os.environ['AWS_ACCESS_KEY_ID'] = self.aws_access_key_id
      os.environ['AWS_SECRET_ACCESS_KEY'] = self.aws_secret_access_key
      os.environ['AWS_REGION'] = self.aws_region
      snt_cmd = 'aws ec2 describe-security-groups --filter "Name=group-id,Values={0}" --output json'.format(self.security_group)
      p = subprocess.run(snt_cmd, shell = True, capture_output = True)
      o = p.stdout.decode()
      e = p.stderr.decode()

      if p.returncode > 0:
        retorno = False
      else:
        if p.stderr.decode() == '':
          t = json.loads(p.stdout.decode())
          retorno = len(t.get('SecurityGroups')) > 0
        else:
          retorno = False
          print(p.stderr.decode())
    except Exception as e:
      retorno = False
      print(traceback.format_exc())

    return retorno


  def check_programa(self):
    retorno = True

    try:
      p = subprocess.run('whereis aws', shell = True, capture_output = True)
      o = p.stdout.decode()
      e = p.stderr.decode()

      if p.returncode > 0:
        retorno = False
      else:
        if p.stderr.decode() == '':
          partes = p.stdout.decode().split(" ")
          retorno = len(partes) > 1
        else:
          retorno = False
          print(p.stderr.decode())
    except Exception as e:
      retorno = False
      print(traceback.format_exc())

    return retorno

  def check_credenciais(self):
    retorno = True

    try:
      os.environ['AWS_ACCESS_KEY_ID'] = self.aws_access_key_id
      os.environ['AWS_SECRET_ACCESS_KEY'] = self.aws_secret_access_key
      os.environ['AWS_REGION'] = self.aws_region

      p = subprocess.run('aws ecr get-login-password', shell = True, capture_output = True)
      o = p.stdout.decode()
      e = p.stderr.decode()

      if p.returncode > 0:
        retorno = False
    except Exception as e:
      retorno = False
      print(traceback.format_exc())

    return retorno

  def check_acesso_ecs(self):
    retorno = True

    try:
      os.environ['AWS_ACCESS_KEY_ID'] = self.aws_access_key_id
      os.environ['AWS_SECRET_ACCESS_KEY'] = self.aws_secret_access_key
      os.environ['AWS_REGION'] = self.aws_region

      p = subprocess.run('aws ecs list-clusters  --output json', shell = True, capture_output = True)
      o = p.stdout.decode()
      e = p.stderr.decode()

      if p.returncode > 0:
        retorno = False
      else:
        self.lista_de_clusters.clear()

        lista_de_clusters = json.loads(p.stdout.decode())

        for i in lista_de_clusters.get('clusterArns'):
          partes = i.split('/')

          if len(partes) > 1:
            self.lista_de_clusters[partes[1]] = i

        retorno = len(self.lista_de_clusters) > 0
    except Exception as e:
      retorno = False
      print(traceback.format_exc())

    return retorno

  def check(self):
    retorno = {
      'grupo_de_seguranca' : {'funcao' : self.check_security_group, 'resulado' : False},
      'subnet' : {'funcao' : self.check_subnet, 'resulado' : False},
      'programa' : {'funcao' : self.check_programa, 'resulado' : False},
      'credencial' : {'funcao' : self.check_credenciais, 'resulado' : False},
      'ecs' : {'funcao' : self.check_acesso_ecs, 'resulado' : False},
      'geral' : True,
      'falhas' : []
    }

    for i in ['grupo_de_seguranca', 'subnet', 'programa', 'credencial', 'ecs']:
      print('Testando {0}...'.format(i))
      retorno.get(i)['resulado'] = retorno.get(i).get('funcao')()

      if retorno.get(i).get('resulado') == False:
        retorno['geral'] = False
        retorno.get('falhas').append(i)

    return {
      'geral' : retorno.get('geral'),
      'falhas' : retorno.get('falhas')
    }

  def validar(self, task_id, cluster = None):
    t = task_id
    c = cluster

    if c == None:
      c = self.cluster

    os.environ['AWS_ACCESS_KEY_ID'] = self.aws_access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = self.aws_secret_access_key
    os.environ['AWS_REGION'] = self.aws_region
    aws_ecs_cmd = 'aws ecs describe-tasks --cluster {0} --task "{1}" --output json'.format(c, t)
    p = subprocess.run(aws_ecs_cmd, shell = True, capture_output = True)
    situacao = "ERRO"

    if p.returncode == 0:
      d = json.loads(p.stdout.decode())

      if len(d.get('tasks')) > 0:
        situacao = d.get('tasks')[0].get('lastStatus')
      else:
        situacao = "STOPPED"

    return situacao

  def anexar(self, cluster = None, task = None, forcar_check = False, monitorar = 30):
    retorno = False
    r = {'geral' : True, 'falhas' : []}

    if self.valido == False or forcar_check:
      r = self.check()
      self.valido = r.get('geral')

    if r.get('geral') == False:
      print('Falhas em:')

      for i in r.get('falhas'):
        print(' * {0}'.format(i))
    else:
      c = cluster
      t = task

      if c == None:
        c = self.cluster

      if t == None:
        t = self.task

      task_id = None
      task_status = "STOPPED"

      cmd_ecs = 'aws ecs list-tasks --cluster {0} --output json'.format(c)
      p = subprocess.run(cmd_ecs, shell = True, capture_output = True)

      if p.returncode == 0:
        d = json.loads(p.stdout.decode())

        if len(d.get('taskArns')) > 0:
          for j in d.get('taskArns'):
            cmd_ecs = 'aws ecs describe-tasks --cluster {0} --task "{1}" --output json'.format(c, j)
            p = subprocess.run(cmd_ecs, shell = True, capture_output = True)

            if p.returncode == 0:
              i = json.loads(p.stdout.decode())

              if re.search(t, i.get('tasks')[0].get('taskDefinitionArn')):
                task_id = j
                task_status = i.get('tasks')[0].get('lastStatus')
                break

          if task_id:
            if task_status in ["PENDING", "RUNNING", "PROVISIONING"]:
              retorno = True
              print("Encontrado situacao corrente {0} para task {1}".format(task_status, task_id))
              continuar = True

              while continuar:
                task_status = self.validar(task_id, c)
                print("Situacao {0}".format(task_status))

                continuar = task_status in ["PENDING", "RUNNING", "PROVISIONING"]

                if continuar:
                  time.sleep(monitorar)
            else:
              print("Situacao STOPPED")
        else:
          print('Nao existe task para o cluster {0}.'.format(c))
      else:
        print(p.stderr.decode())

    return retorno
 
  def executar(self, forcar_check = False, cluster = None, task = None, monitorar = 30):
    alguma_rotina_ativa = self.anexar(cluster, task, forcar_check, monitorar)

    if alguma_rotina_ativa == False:
      r = {'geral' : True, 'falhas' : []}

      if self.valido == False or forcar_check:
        r = self.check()
        self.valido = r.get('geral')

      if r.get('geral') == False:
        print('Falhas em:')

        for i in r.get('falhas'):
          print(' * {0}'.format(i))
      else:
        c = cluster
        t = task

        if t == None:
          t = self.task

        if c == None:
          c = self.cluster

        if c in self.lista_de_clusters:
          os.environ['AWS_ACCESS_KEY_ID'] = self.aws_access_key_id
          os.environ['AWS_SECRET_ACCESS_KEY'] = self.aws_secret_access_key
          os.environ['AWS_REGION'] = self.aws_region
          aws_ecs_cfg = 'aws ecs run-task  --cluster ' + c + ' --task-definition ' + t + ' --launch-type="FARGATE" --network-configuration'
          aws_ecs_ntw = ' \'{ "awsvpcConfiguration" : { "assignPublicIp" : "ENABLED" , "securityGroups" : ["' + self.security_group + '"], "subnets" : ["' + self.subnet + '"] } }\''
          aws_ecs_cmd = aws_ecs_cfg + aws_ecs_ntw
          p = subprocess.run(aws_ecs_cmd, shell = True, capture_output = True)

          if p.returncode == 0:
            r = json.loads(p.stdout.decode())
            t_id = r.get('tasks')[0].get('taskArn')

            if monitorar > 0:
              continuar = True

              while continuar:
                situacao = self.validar(c, t_id)
                print('Situacao: {0}'.format(situacao))
                continuar = situacao in ["RUNNING", "PENDING", "PROVISIONING"]

                if continuar:
                  time.sleep(monitorar)
            else:
              arq = None
              arq_nome = '/tmp/ecs.{0}.info'.format(t)

              try:
                arq = open(arq_nome, 'w')
                arq.write(t_id)
              except Exception as e:
                print('Não foi possível criar o arquivo em {0}. Tarefa gerada com o identificador {1}'.format(arq_nome, t_id))
              finally:
                if arq != None:
                  arq.close()
          else:
            print(p.stderr.decode())
        else:
          print('Cluster informado {0} nao esta na lista de cluster ECS.')
