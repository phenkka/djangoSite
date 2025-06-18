from django.db import models

class MainPageInfo(models.Model):
    profession_name = models.CharField()
    greeting_img = models.ImageField(upload_to='main_images/')
    greeting_description = models.TextField()

    header_1 = models.CharField(blank=True, null=True)
    under_header_1 = models.CharField(blank=True, null=True)
    under_1_1 = models.CharField(blank=True, null=True)
    under_1_2 = models.CharField(blank=True, null=True)
    under_1_3 = models.CharField(blank=True, null=True)
    under_1_4 = models.CharField(blank=True, null=True)

    under_header_2 = models.CharField(blank=True, null=True)
    under_2_1 = models.CharField(blank=True, null=True)
    under_2_2 = models.CharField(blank=True, null=True)
    under_2_3 = models.CharField(blank=True, null=True)

    under_header_3 = models.CharField(blank=True, null=True)
    under_3_1 = models.CharField(blank=True, null=True)
    under_3_2 = models.CharField(blank=True, null=True)
    under_3_3 = models.CharField(blank=True, null=True)

    under_header_4 = models.CharField(blank=True, null=True)
    under_4_1 = models.CharField(blank=True, null=True)
    under_4_2 = models.CharField(blank=True, null=True)
    under_4_3 = models.CharField(blank=True, null=True)

    additional_info_name = models.CharField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    additional_img = models.ImageField(upload_to='main_images/')

    def __str__(self):
        return self.profession_name

class GeneralStatistics(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание (опционально)", blank=True)
    under_1 = models.CharField(blank=True, null=True)
    under_2 = models.CharField(blank=True, null=True)
    under_3 = models.CharField(blank=True, null=True)
    under_4 = models.CharField(blank=True, null=True)
    under_5 = models.CharField(blank=True, null=True)
    ending = models.TextField(verbose_name="Описание (опционально)", blank=True, null=True)

    salary_dynamics = models.ImageField(upload_to='charts/', verbose_name="Динамика уровня зарплат по годам", blank=True, null=True)
    vacancies_dynamics = models.ImageField(upload_to='charts/', verbose_name="Динамика количества вакансий по годам", blank=True, null=True)
    salary_by_city = models.ImageField(upload_to='charts/', verbose_name="Уровень зарплат по городам", blank=True, null=True)
    vacancies_share_by_city = models.ImageField(upload_to='charts/', verbose_name="Доля вакансий по городам", blank=True, null=True)
    top_skills = models.ImageField(upload_to='charts/', verbose_name="ТОП-20 навыков по годам", blank=True, null=True)

    salary_dynamics_csv = models.FileField(upload_to='csv/', verbose_name="CSV: Динамика зарплат", blank=True, null=True)
    vacancies_dynamics_csv = models.FileField(upload_to='csv/', verbose_name="CSV: Динамика вакансий", blank=True, null=True)
    salary_by_city_csv = models.FileField(upload_to='csv/', verbose_name="CSV: Зарплаты по городам", blank=True, null=True)
    vacancies_share_by_city_csv = models.FileField(upload_to='csv/', verbose_name="CSV: Доля вакансий по городам", blank=True, null=True)
    top_skills_csv = models.FileField(upload_to='csv/', verbose_name="CSV: ТОП-20 навыков", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Общая статистика"
        verbose_name_plural = "Общая статистика"


class DemandStatistics(models.Model):
    title = models.CharField(max_length=200, default='Востребованность iOS-разработчика')
    description = models.TextField(blank=True)
    under_1 = models.CharField(blank=True, null=True)
    under_2 = models.CharField(blank=True, null=True)
    ending = models.TextField(verbose_name="Описание (опционально)", blank=True, null=True)

    ios_salary_level_trend = models.ImageField(upload_to='charts/', verbose_name="Динамика уровня зарплат по годам для выбранной профессии")
    ios_vacancies_level_trend = models.ImageField(upload_to='charts/', verbose_name="Динамика количества вакансий по годам для выбранной профессии")

    ios_salary_level_trend_csv = models.FileField(upload_to='csv/', verbose_name="CSV: Динамика уровня зарплат по годам для выбранной профессии", blank=True, null=True)
    ios_vacancies_level_trend_csv = models.FileField(upload_to='csv/', verbose_name="CSV: Динамика количества вакансий по годам для выбранной профессии", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Востребованность"
        verbose_name_plural = "Востребованность"


class GeoStatistics(models.Model):
    title = models.CharField(max_length=200, default='География iOS-разработчика')
    description = models.TextField(blank=True)
    under_1 = models.CharField(blank=True, null=True)
    under_2 = models.CharField(blank=True, null=True)
    ending = models.TextField(verbose_name="Описание (опционально)", blank=True, null=True)

    geo_ios_city_salary = models.ImageField(upload_to='charts/', verbose_name="Уровень зарплат по городам для выбранной профессии")
    geo_ios_city_vacancy_share = models.ImageField(upload_to='charts/', verbose_name="Доля вакансий по городам для выбранной профессии")

    geo_ios_city_salary_csv = models.FileField(upload_to='csv/', verbose_name="CSV: Уровень зарплат по городам для выбранной профессии", blank=True, null=True)
    geo_ios_city_vacancy_share_csv = models.FileField(upload_to='csv/', verbose_name="CSV: Доля вакансий по городам для выбранной профессии", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "География"
        verbose_name_plural = "География"



class SkillsStatistics(models.Model):
    title = models.CharField(max_length=200, default='ТОП-20 навыков для iOS-разработчика')
    description = models.TextField(blank=True)
    under_1 = models.CharField(blank=True, null=True)
    ending = models.TextField(verbose_name="Описание (опционально)", blank=True, null=True)

    skills_top_ios_trend = models.ImageField(upload_to='charts/', verbose_name="ТОП-20 навыков по годам для выбранной профессии")
    skills_top_ios_trend_csv = models.FileField(upload_to='csv/', verbose_name="CSV: ТОП-20 навыков по годам для выбранной профессии", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Навыки"
        verbose_name_plural = "Навыки"

class HHStatistics(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=310)
    skills_str = models.CharField()
    company = models.CharField()
    salary = models.CharField()
    area = models.CharField()
    published_at = models.DateTimeField()
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name