import boto3
import uuid

def seed_institutions():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('institutions-dev')

    # Delete existing items first
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan.get('Items', []):
            batch.delete_item(Key={'cnpj': each['cnpj']})
    print("Old items deleted.")

    institutions = [
        {
            "cnpj": "11111111000111",
            "name": "Instituto Ação Cidadã",
            "email": "contato@acaocidada.org.br",
            "phone_number": "11999999999",
            "region": "Sudeste",
            "state": "SP",
            "address": "Rua da Solidariedade",
            "city": "São Paulo",
            "neighborhood": "Centro",
            "cep": "01001000",
            "address_number": 100,
            "about": "Focados em combater a fome e promover cidadania em comunidades vulneráveis de São Paulo. Distribuímos cestas básicas e oferecemos cursos profissionalizantes.",
            "site": "https://www.acaocidada.org.br",
            "confirmation_audio": "https://s3.amazonaws.com/bucket/audio1.mp3",
            "image": "https://s3.amazonaws.com/bucket/image1.jpg",
            "verified": True,
            "token": str(uuid.uuid4())
        },
        {
            "cnpj": "22222222000122",
            "name": "Teto e Vida",
            "email": "ajuda@tetoevida.org.br",
            "phone_number": "21988888888",
            "region": "Sudeste",
            "state": "RJ",
            "address": "Avenida Esperança",
            "city": "Rio de Janeiro",
            "neighborhood": "Copacabana",
            "cep": "22000000",
            "address_number": 500,
            "about": "Nossa missão é construir abrigos emergenciais e apoiar pessoas em situação de rua no estado do Rio de Janeiro com alimentação e apoio psicológico.",
            "site": "https://www.tetoevida.org.br",
            "confirmation_audio": "https://s3.amazonaws.com/bucket/audio2.mp3",
            "image": "https://s3.amazonaws.com/bucket/image2.jpg",
            "verified": True,
            "token": str(uuid.uuid4())
        },
        {
            "cnpj": "33333333000133",
            "name": "Sertão Verde",
            "email": "contato@sertaoverde.org.br",
            "phone_number": "81977777777",
            "region": "Nordeste",
            "state": "PE",
            "address": "Rua do Sol",
            "city": "Recife",
            "neighborhood": "Boa Vista",
            "cep": "50000000",
            "address_number": 30,
            "about": "Projeto que leva cisternas e sistemas de irrigação sustentável para famílias afetadas pela seca no sertão nordestino, promovendo a agricultura familiar.",
            "site": "https://www.sertaoverde.org.br",
            "confirmation_audio": "https://s3.amazonaws.com/bucket/audio3.mp3",
            "image": "https://s3.amazonaws.com/bucket/image3.jpg",
            "verified": True,
            "token": str(uuid.uuid4())
        },
        {
            "cnpj": "44444444000144",
            "name": "Patinhas do Bem",
            "email": "adocao@patinhasdobem.com.br",
            "phone_number": "41966666666",
            "region": "Sul",
            "state": "PR",
            "address": "Rua das Flores",
            "city": "Curitiba",
            "neighborhood": "Batel",
            "cep": "80000000",
            "address_number": 255,
            "about": "Resgate, reabilitação e adoção de cães e gatos abandonados. Mantemos um abrigo seguro e campanhas mensais de castração gratuita.",
            "site": "https://www.patinhasdobem.com.br",
            "confirmation_audio": "https://s3.amazonaws.com/bucket/audio4.mp3",
            "image": "https://s3.amazonaws.com/bucket/image4.jpg",
            "verified": True,
            "token": str(uuid.uuid4())
        },
        {
            "cnpj": "55555555000155",
            "name": "EducaTech Brasil",
            "email": "parcerias@educatech.org.br",
            "phone_number": "61955555555",
            "region": "Centro-Oeste",
            "state": "DF",
            "address": "Via Eixo Monumental",
            "city": "Brasília",
            "neighborhood": "Asa Sul",
            "cep": "70000000",
            "address_number": 12,
            "about": "Democratizando o acesso à tecnologia. Oferecemos aulas gratuitas de programação e robótica para jovens de escolas públicas do Distrito Federal.",
            "site": "https://www.educatech.org.br",
            "confirmation_audio": "https://s3.amazonaws.com/bucket/audio5.mp3",
            "image": "https://s3.amazonaws.com/bucket/image5.jpg",
            "verified": True,
            "token": str(uuid.uuid4())
        }
    ]

    for inst in institutions:
        inst['id'] = str(uuid.uuid4())
        print(f"Inserindo: {inst['name']}")
        table.put_item(Item=inst)

if __name__ == '__main__':
    seed_institutions()
