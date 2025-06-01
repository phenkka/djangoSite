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
