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
    salary_graph = models.ImageField(upload_to='charts/', verbose_name="График зарплат по годам")
    vacancy_graph = models.ImageField(upload_to='charts/', verbose_name="График количества вакансий по годам")
    salary_table = models.TextField(verbose_name="HTML-таблица зарплат по годам")
    vacancy_table = models.TextField(verbose_name="HTML-таблица количества вакансий по годам")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Общая статистика"
        verbose_name_plural = "Общая статистика"
