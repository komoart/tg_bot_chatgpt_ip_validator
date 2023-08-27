import pandas as pd
from ipwhois import IPWhois


class Worker_csv:

    def reader_csv(self, path_from_csv: str) -> list[str]:
        df_from_csv = pd.read_csv(path_from_csv)
        ip_list_from_csv = df_from_csv['ip'].tolist()
        return ip_list_from_csv

    def writer_csv(self, path_to_csv: str, ip_list_to_csv: list[str], provider_list: list[str]):
        df_to_csv = pd.DataFrame(
            {
                'ip': ip_list_to_csv,
                'provider': provider_list
            }
        )
        df_to_csv.to_csv(path_to_csv, sep=';', index=False)


class Definer_provider:
    def get_ip_provider(self, ip_address: str) -> str:
        try:
            obj = IPWhois(ip_address)
            response = obj.lookup_rdap()
            provider = response['asn_description']
            return provider
        except Exception as e:
            print(f"Error: {e}")
            return "Не определен"

    def define_provider(self, list_ip_addresses: list[str]):
        providers = []
        for i in list_ip_addresses:
            providers.append(self.get_ip_provider(i))
        return providers


class Check_IP:
    def make_ip_binary(self, ip: str) -> str:
        ip_octets = ip.split(".")
        ip_binary = "".join([bin(int(octet))[2:].zfill(8) for octet in ip_octets])
        return ip_binary

    def check_ip(self, ip_network: str, ip_subnet: str, list_ip: list[str]) -> str | list[str]:
        ip_network_binary = self.make_ip_binary(ip_network)
        ip_subnet_binary = self.make_ip_binary(ip_subnet)
        subnet_prefix_length = ip_subnet_binary.count("1")

        for i in range(1, len(ip_subnet_binary)):
            if int(ip_subnet_binary[i]) - int(ip_subnet_binary[i - 1]) == 1:
                return "Маска введена неверно"
        if ip_network_binary[subnet_prefix_length:] != ip_subnet_binary[subnet_prefix_length:]:
            return "Адрес сети не подходит к маске подсети"

        list_ip_checked = []
        for i in list_ip:
            if self.make_ip_binary(i)[:subnet_prefix_length] == ip_network_binary[:subnet_prefix_length]:
                list_ip_checked.append(i)
        return list_ip_checked


def main():
    print("Введите имя csv-файла (без типа) с ip-адресами: ")
    file_name_csv = input()
    ips_input = Worker_csv().reader_csv(f"{file_name_csv}.csv")
    print("Введите маску подсети в формате IPv4: ")
    ip_subnet = input()
    print("Введите адрес сети в формате  IPv4: ")
    ip_network = input()
    ips_output = Check_IP().check_ip(ip_network, ip_subnet, ips_input)
    providers = Definer_provider().define_provider(ips_output)
    print("Введите имя для сохранения csv-файла: ")
    csv_output = input()
    Worker_csv().writer_csv(f"{csv_output}.csv", ips_output, providers)


if __name__ == '__main__':
    main()
