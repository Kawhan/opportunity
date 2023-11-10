from project.models import vagasEmprego


class Start:
    def define_data_info(data: dict):
        data['alunos_SI_iniciacao_tecnologica'] = 0
        data['alunos_LCC_iniciacao_tecnologica'] = 0

        data['alunos_SI_iniciacao_cientifica'] = 0
        data['alunos_LCC_iniciacao_cientifica'] = 0

        data['alunos_SI_extensao'] = 0
        data['alunos_LCC_extensao'] = 0

        data['alunos_SI_estagio'] = 0
        data['alunos_LCC_estagio'] = 0

        data['alunos_SI_desenvolvimento'] = 0
        data['alunos_LCC_desenvolvimento'] = 0

        return data

    def define_info_count_from_jobs(data: dict):
        data['PIT'] = vagasEmprego.objects.filter(tipo_vaga='PIT').count()
        data['PIC'] = vagasEmprego.objects.filter(tipo_vaga='PIC').count()
        data['PE'] = vagasEmprego.objects.filter(tipo_vaga='PE').count()
        data['ES'] = vagasEmprego.objects.filter(tipo_vaga='ES').count()
        data['PD'] = vagasEmprego.objects.filter(tipo_vaga='PD').count()

        return data

    def query_set_info_from_jobs(query_set_data: dict):
        query_set_data['queryset_iniciacao_tecnologica'] = vagasEmprego.objects.filter(
            tipo_vaga='PIT')
        query_set_data['queryset_iniciacao_cientifica'] = vagasEmprego.objects.filter(
            tipo_vaga='PIC')
        query_set_data['queryset_extensao'] = vagasEmprego.objects.filter(
            tipo_vaga='PE')
        query_set_data['queryset_estagio'] = vagasEmprego.objects.filter(
            tipo_vaga='ES')
        query_set_data['queryset_desenvolvimento'] = vagasEmprego.objects.filter(
            tipo_vaga='PD')

        return query_set_data

    def cal_info_students_in_extension_project(query_set_data: dict, data: dict):
        for extensao in query_set_data['queryset_extensao']:
            for aluno in extensao.aluno.values().distinct():
                if aluno['curso'] == 'SI':
                    data['alunos_SI_extensao'] += 1
                elif aluno['curso'] == 'LCC':
                    data['alunos_LCC_extensao'] += 1

        return {
            'data': data
        }

    def cal_info_stundents_in_research_technological_project(query_set_data: dict, data: dict):
        for tech in query_set_data['queryset_iniciacao_tecnologica']:
            for aluno in tech.aluno.values().distinct():
                if aluno['curso'] == 'SI':
                    data['alunos_SI_iniciacao_tecnologica'] += 1
                if aluno['curso'] == 'LCC':
                    data['alunos_LCC_iniciacao_tecnologica'] += 1

        return {
            'data': data
        }

    def cal_info_stundents_in_research_scientific_project(query_set_data: dict, data: dict):
        for scientific in query_set_data['queryset_iniciacao_cientifica']:
            for aluno in scientific.aluno.values().distinct():
                if aluno['curso'] == 'SI':
                    data['alunos_SI_iniciacao_cientifica'] += 1
                if aluno['curso'] == 'LCC':
                    data['alunos_LCC_iniciacao_cientifica'] += 1

        return {
            'data': data
        }

    def cal_info_students_in_intern(query_set_data: dict, data: dict):
        for estagio in query_set_data['queryset_estagio']:
            for aluno in estagio.aluno.values().distinct():
                if aluno['curso'] == 'SI':
                    data['alunos_SI_estagio'] += 1
                elif aluno['curso'] == 'LCC':
                    data['alunos_LCC_estagio'] += 1

        return {
            'data': data
        }

    def cal_info_students_in_developer(query_set_data: dict, data: dict):
        for desenvolvimento in query_set_data['queryset_desenvolvimento']:
            for aluno in desenvolvimento.aluno.values().distinct():
                if aluno['curso'] == 'SI':
                    data['alunos_SI_desenvolvimento'] += 1
                elif aluno['curso'] == 'LCC':

                    data['alunos_LCC_desenvolvimento'] += 1

        return {
            'data': data
        }


class IndividualStart:
    def define_data_info(data: dict):
        data['alunos_SI'] = 0
        data['alunos_LCC'] = 0

        data['inscricoes_SI'] = 0
        data['inscricoes_LCC'] = 0

        return data

    def define_info_count_from_jobs(data: dict, vaga_id: int):
        data['vagas'] = vagasEmprego.objects.filter(
            id=vaga_id).values('numeroVagas')
        data['vagas'] = data['vagas'][0]['numeroVagas']
        data['vaga_object'] = vagasEmprego.objects.filter(
            id=vaga_id)

        return data

    def info_subscribe_in_job(data: dict, alunos: list):
        query_set_data = data['vaga_object']

        for alunos_curso in query_set_data:
            for aluno in alunos_curso.aluno.values().distinct():
                if aluno['curso'] == 'SI' and aluno not in alunos:
                    alunos.append(aluno)
                    data['alunos_SI'] += 1
                elif aluno['curso'] == 'LCC' and aluno not in alunos:
                    alunos.append(aluno)
                    data['alunos_LCC'] += 1

        return {
            'alunos': alunos,
            'data': data
        }

    # def all_subscribe_in_job(data: dict):
    #     query_set_data = data['vaga_object']

    #     for info in query_set_data:
    #         for aluno in info.aluno.values().distinct():
    #             if aluno['curso'] == 'SI':
    #                 data['inscricoes_SI'] += 1
    #             elif aluno['curso'] == 'LCC':
    #                 data['inscricoes_LCC'] += 1

    #     return {
    #         'data': data
    #     }

        pass
