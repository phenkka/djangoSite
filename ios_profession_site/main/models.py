from django.db import models

class MainPageInfo(models.Model):
    profession_name = models.CharField(max_length=100, default='iOS-разработчик')
    description = models.TextField()
    image = models.ImageField(upload_to='main_images/')

    def __str__(self):
        return self.profession_name

class GeneralStatistics(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание (опционально)", blank=True)
    salary_dynamics = models.ImageField(upload_to='charts/', verbose_name="Динамика уровня зарплат по годам", blank=True, null=True)
    vacancies_dynamics = models.ImageField(upload_to='charts/', verbose_name="Динамика количества вакансий по годам", blank=True, null=True)
    salary_by_city = models.ImageField(upload_to='charts/', verbose_name="Уровень зарплат по городам", blank=True, null=True)
    vacancies_share_by_city = models.ImageField(upload_to='charts/', verbose_name="Доля вакансий по городам", blank=True, null=True)
    top_skills = models.ImageField(upload_to='charts/', verbose_name="ТОП-20 навыков по годам", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Общая статистика"
        verbose_name_plural = "Общая статистика"


class DemandStatistics(models.Model):
    title = models.CharField(max_length=200, default='Востребованность iOS-разработчика')
    description = models.TextField(blank=True)

    ios_salary_level_trend = models.ImageField(upload_to='charts/', verbose_name="Динамика уровня зарплат по годам для выбранной профессии")
    ios_vacancies_level_trend = models.ImageField(upload_to='charts/', verbose_name="Динамика количества вакансий по годам для выбранной профессии")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Востребованность"
        verbose_name_plural = "Востребованность"


class GeoStatistics(models.Model):
    title = models.CharField(max_length=200, default='География iOS-разработчика')
    description = models.TextField(blank=True)

    geo_ios_city_salary = models.ImageField(upload_to='charts/', verbose_name="Уровень зарплат по городам для выбранной профессии")
    geo_ios_city_vacancy_share = models.ImageField(upload_to='charts/', verbose_name="Доля вакансий по городам для выбранной профессии")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "География"
        verbose_name_plural = "География"