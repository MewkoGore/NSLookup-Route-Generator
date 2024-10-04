import subprocess

def nslookup(domain):
    """Выполняет nslookup для указанного домена и возвращает второй IP-адрес."""
    try:
        # Выполняем nslookup
        output = subprocess.check_output(['nslookup', domain], stderr=subprocess.STDOUT)
        output = output.decode('cp1251')  # Используйте 'utf-8', если это необходимо
        # Извлекаем IP-адреса из вывода
        ip_addresses = []
        for line in output.splitlines():
            if 'Address:' in line:
                ip = line.split('Address: ')[1].strip()
                ip_addresses.append(ip)
        # Возвращаем только второй IP, если он существует
        return ip_addresses[1] if len(ip_addresses) > 1 else None
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении nslookup для {domain}: {e.output.decode('cp1251')}")
        return None

def main():
    input_file = 'domains.txt'  # Файл с доменами
    output_file = 'routes.rsc'  # Файл для записи команд MikroTik

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for domain in infile:
            domain = domain.strip()
            if domain:
                ip = nslookup(domain)
                if ip:
                    # Формируем команду для добавления маршрута с комментарием
                    command = f"/ip route add dst-address={ip}/32 gateway=93.170.163.254 comment=\"voidboost_cdn\"\n"
                    outfile.write(command)
                    print(f"Обработан домен: {domain}, Второй IP: {ip}")
                else:
                    print(f"Не удалось получить второй IP для домена: {domain}")

if __name__ == '__main__':
    main()
